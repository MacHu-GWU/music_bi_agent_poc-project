# -*- coding: utf-8 -*-

from .one.api import one
from rich import print as rprint


def run_agent(user_input: str) -> str:
    """
    Multi-agent orchestration workflow for handling user queries.

    This function implements a two-tier agent architecture:
    1. Router Agent: Analyzes the query and delegates to specialized agents (SQL, Knowledge)
    2. Report Agent: Synthesizes all intermediate results into a polished final answer

    :param user_input: The user's natural language query

    :return: Final synthesized answer as a string

    Workflow:
        User Query → Router Agent (with sql_assistant & knowledge_assistant tools)
                  → Report Agent → Final Answer
    """
    # Step 1: Router Agent orchestrates and delegates to specialists
    # The router analyzes the query and decides:
    # - Answer directly if it's a simple general question
    # - Call sql_assistant for database/analytics queries
    # - Call knowledge_assistant for documentation/code queries
    # - Call both if needed for hybrid questions
    router_response = one.router_agent(user_input)

    # Step 2: Report Agent synthesizes the final answer
    # Takes the original query and router's intermediate results
    # Produces a well-formatted, comprehensive final response
    report_prompt = f"""The user asked: "{user_input}"

Intermediate analysis and results:
{router_response}

Your task: Create a polished, comprehensive final answer that addresses all aspects of the user's question. Use proper formatting, structure the information clearly, and ensure nothing important is lost."""

    final_response = one.report_agent(report_prompt)

    return str(final_response)
