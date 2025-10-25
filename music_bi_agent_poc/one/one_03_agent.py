# -*- coding: utf-8 -*-

import typing as T
from functools import cached_property

import strands

from ..paths import path_enum

if T.TYPE_CHECKING:  # pragma: no cover
    from .one_01_main import One


class AgentMixin:
    @strands.tool
    def sql_assistant(self: "One", query: str) -> str:
        """
        SQL database analysis assistant for querying the Chinook music store database.

        Use this tool when you need to:
        - Query transactional sales data
        - Analyze revenue, trends, and performance metrics
        - Get top performers (artists, tracks, genres, customers)
        - Retrieve specific numbers and data-driven insights

        The assistant has access to tables including: Invoice, InvoiceLine, Track,
        Album, Artist, Genre, and Customer. It can execute SELECT queries and
        provide detailed analytical results.

        :param query: Natural language query about database analytics. Should include
                     the instruction "Run SQL if needed: [your question]" followed by
                     guidance to use available tools properly.

        :return: String containing SQL query executed, results, and analysis.

        Example usage:
            query = "Run SQL if needed: 'Which artist has the highest sales?'. Use your available tools to write SQL (SELECT ONLY), run SQL, and interpret SQL results properly."
        """
        response = self.sql_agent(query)
        return str(response)

    @strands.tool
    def knowledge_assistant(self: "One", query: str) -> str:
        """
        Knowledge base retrieval assistant for project documentation and codebase information.

        Use this tool when you need to:
        - Find documentation about the project
        - Locate code files or understand project structure
        - Learn how to use features, run tests, or configure the system
        - Get information about implementation details and APIs

        The assistant searches through a comprehensive knowledge base containing
        source code, documentation, guides, and repository information using
        semantic vector search.

        :param query: Natural language query about project knowledge. Should include
                     the instruction "Retrieve knowledge if needed: [your question]"
                     followed by guidance to use available tools.

        :return: String containing relevant documentation and code references.

        Example usage:
            query = "Retrieve knowledge if needed: 'How to run the test suite?'. Use your available tools to retrieve relevant information from knowledge base."
        """
        response = self.knowledge_agent(query)
        return str(response)

    @cached_property
    def router_agent(self: "One") -> strands.Agent:
        return strands.Agent(
            model=self.model,
            system_prompt=path_enum.path_prompts_router.read_text(),
            callback_handler=None,  # Suppress intermediate output for cleaner UX
            tools=[
                self.sql_assistant,
                self.knowledge_assistant,
            ],
        )

    @cached_property
    def sql_agent(self: "One") -> strands.Agent:
        return strands.Agent(
            model=self.model,
            system_prompt=path_enum.path_prompts_sql_agent.read_text(),
            # callback_handler=None,
            tools=[
                self.list_databases,
                self.list_tables,
                self.get_all_database_details,
                self.get_schema_details,
                self.execute_select_statement,
            ],
        )

    @cached_property
    def knowledge_agent(self: "One") -> strands.Agent:
        return strands.Agent(
            model=self.model,
            system_prompt=path_enum.path_prompts_knowledge.read_text(),
            # callback_handler=None,
            tools=[
                self.retrieve_knowledge,
            ],
        )

    @cached_property
    def report_agent(self: "One") -> strands.Agent:
        return strands.Agent(
            model=self.model,
            system_prompt=path_enum.path_prompts_report.read_text(),
            # callback_handler=None,
            tools=[],
        )
