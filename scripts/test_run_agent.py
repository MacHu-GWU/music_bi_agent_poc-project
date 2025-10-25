# -*- coding: utf-8 -*-

from music_bi_agent_poc.agent import run_agent
from rich import print as rprint

def example_1():
    user_input = """
    Tell me about what table do I have in the database.
    """.strip()

    sql_agent_response = run_agent(
        f"Run SQL if needed: '{user_input}'. Use your available tools to write SQL (SELECT ONLY), run SQL, and interprete SQL results properly.",
    )
    rprint(sql_agent_response)

example_1()
