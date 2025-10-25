# -*- coding: utf-8 -*-

import typing as T
from functools import cached_property

from boto_session_manager import BotoSesManager
import strands
from s3pathlib import S3Path
import s3vectorm.api as s3vectorm

if T.TYPE_CHECKING:  # pragma: no cover
    from .one_01_main import One


class AwsMixin:
    @cached_property
    def bsm(self: "One") -> BotoSesManager:
        return BotoSesManager(profile_name="esc_app_dev_us_east_1")

    @cached_property
    def model(self: "One") -> strands.models.BedrockModel:
        return strands.models.BedrockModel(
            # model_id="us.amazon.nova-pro-v1:0",
            model_id="us.amazon.nova-lite-v1:0",
            boto_session=self.bsm.boto_ses,
        )

    @cached_property
    def vector_bucket(self) -> s3vectorm.Bucket:
        return s3vectorm.Bucket(
            name="music-bi-agent-poc",
        )

    @cached_property
    def vector_index(self) -> s3vectorm.Index:
        return s3vectorm.Index(
            bucket_name=self.vector_bucket.name,
            index_name="knowledge-base",
            data_type="float32",
            dimension=768,  # Common dimension for many LLM embeddings
            distance_metric="cosine",
        )
