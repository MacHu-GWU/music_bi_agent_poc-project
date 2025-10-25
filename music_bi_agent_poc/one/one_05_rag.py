# -*- coding: utf-8 -*-

import typing as T
import re
import hashlib
from functools import cached_property

import strands
from s3pathlib import S3Path
from s3vectorm.api import Vector
from fastembed import TextEmbedding

from ..paths import path_enum

if T.TYPE_CHECKING:  # pragma: no cover
    from .one_01_main import One


def parse_all_in_one_knowledge() -> list[str]:
    """
    Parse the XML file and extract all <document> elements.

    :param file_path: Path to the XML file containing <document> elements
    :return: List of strings, each containing a complete <document>...</document> block
    """
    # Read the entire file content
    content = path_enum.path_knowledge_base_txt.read_text()
    # Use regex to find all <document>...</document> blocks
    # re.DOTALL flag allows . to match newlines
    pattern = r"<document>.*?</document>"
    documents = re.findall(pattern, content, re.DOTALL)

    return documents


class DocumentChunk(Vector):
    pass


class RagMixin:
    @cached_property
    def embedding_model(self: "One") -> TextEmbedding:
        return TextEmbedding(
            model_name="BAAI/bge-small-en-v1.5",  # dim = 384
        )

    def batch_embedding(
        self: "One",
        documents: list[str],
    ) -> list[list[float]]:
        return list(self.embedding_model.embed(documents=documents))

    def single_embedding(self: "One", document: str) -> list[float]:
        return self.batch_embedding([document])[0]

    @cached_property
    def s3dir_documents(self: "One") -> S3Path:
        return S3Path(
            f"{self.bsm.aws_account_alias}-{self.bsm.aws_region}-data/projects/music_bi_agent_poc/documents/"
        ).to_dir()

    def get_s3path_doc(self: "One", key: str) -> S3Path:
        return self.s3dir_documents / f"{key}.txt"

    def prepare_knowledge_base(self: "One"):
        self.vector_bucket.create(s3_vectors_client=self.s3vectors_client)
        self.vector_index.create(s3_vectors_client=self.s3vectors_client)
        self.vector_index.delete_all_vectors(s3_vectors_client=self.s3vectors_client)
        chunk_contents = parse_all_in_one_knowledge()
        embeddings_list = self.batch_embedding(chunk_contents)
        vectors = []
        for chunk_content, embedding in zip(chunk_contents, embeddings_list):
            key = hashlib.md5(chunk_content.encode("utf-8")).hexdigest()
            vector = DocumentChunk(
                key=key,
                data=embedding,
            )
            vectors.append(vector)
            s3path = self.get_s3path_doc(key=key)
            s3path.write_text(chunk_content, bsm=self.bsm, content_type="text/plain")
        self.vector_index.put_vectors(
            s3_vectors_client=self.s3vectors_client,
            vectors=vectors,
        )

    @strands.tool
    def retrieve(
        self,
        query: str,
    ) -> list[str]:
        query_embedding = self.single_embedding(query)
        results = self.vector_index.query_vectors(
            s3_vectors_client=self.s3vectors_client,
            data=query_embedding.tolist(),
            top_k=5,
            return_metadata=True,
        )
        vectors = results.as_vector_objects(DocumentChunk)
        chunks = []
        for vector in vectors:
            s3path = self.get_s3path_doc(key=vector.key)
            content = s3path.read_text(bsm=self.bsm)
            chunks.append(content)
        return chunks
