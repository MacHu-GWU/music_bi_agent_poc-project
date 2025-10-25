# -*- coding: utf-8 -*-

from music_bi_agent_poc.one.api import one
from rich import print as rprint

def example_1():
    user_input = """
    Tell me about what table do I have in the database.
    """.strip()

    sql_agent_response = one.sql_agent(
        f"Run SQL if needed: '{user_input}'. Use your available tools to write SQL (SELECT ONLY), run SQL, and interprete SQL results properly.",
    )
    rprint(sql_agent_response)

# example_1()

def example_2():
    user_input = """
    which music track has highest sales? show me the sql statement you use and the your sql execution result in a markdown table
    """.strip()

    sql_agent_response = one.sql_agent(
        f"Run SQL if needed: '{user_input}'. Use your available tools to gather information from reliable sources.",
    )
    rprint(sql_agent_response)

# example_2()
