# -*- coding: utf-8 -*-

from music_bi_agent_poc.one.api import one
from rich import print as rprint

# one.prepare_knowledge_base()

def example_1():
    user_input = """
    which python module defines the agent and it's prompt?
    """

    knowledge_agent_response = one.knowledge_agent(
        f"Retrieve knowledge if needed: '{user_input}'. Use your available tools to retrieve relavant information from knowledge base.",
    )
    rprint(knowledge_agent_response)

example_1()

def example_2()
# chunks = one.retrieve(query="which python module defines the agent and it's prompt?")
# for ith, chunk in enumerate(chunks, start=1):
#     print(f"===== {ith}th =====")
#     print(chunk)
