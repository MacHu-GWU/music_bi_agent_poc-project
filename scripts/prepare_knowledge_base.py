# -*- coding: utf-8 -*-

from music_bi_agent_poc.one.api import one

one.prepare_knowledge_base()

# chunks = one.retrieve(query="which python module defines the agent and it's prompt?")
# for ith, chunk in enumerate(chunks, start=1):
#     print(f"===== {ith}th =====")
#     print(chunk)
