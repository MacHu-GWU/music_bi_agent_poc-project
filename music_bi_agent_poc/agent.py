# -*- coding: utf-8 -*-

from .one.api import one
from rich import print as rprint

def run_agent(user_input: str):
    # Step 1: Researcher Agent gathers web information
    print("===== SQL Agent response =====")
    sql_agent_response = one.sql_agent(
        f"Run SQL if needed: '{user_input}'. Use your available tools to gather information from reliable sources.",
    )
    # rprint(sql_agent_response)
    sql_agent_response_str = str(sql_agent_response)
    return sql_agent_response_str
