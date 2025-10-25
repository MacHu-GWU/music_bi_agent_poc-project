# -*- coding: utf-8 -*-

import typing as T
from functools import cached_property

from boto_session_manager import BotoSesManager
import strands

from mcp_ohmy_sql.config.api import (
    TableFilter,
    Schema,
    SqlalchemyConnection,
    Database,
    Config,
)
from mcp_ohmy_sql.adapter.api import Adapter

from ..paths import path_enum

if T.TYPE_CHECKING:  # pragma: no cover
    from .one_01_main import One


class SqlMixin:

    @cached_property
    def ohmy_sql_config(self: "One"):
        return Config(
            version="0.1.1",
            databases=[
                Database(
                    identifier="chinook sqlite",
                    description="Chinook is a sample database available for SQL Server, Oracle, MySQL, etc. It can be created by running a single SQL script. Chinook database is an alternative to the Northwind database, being ideal for demos and testing ORM tools targeting single and multiple database servers.",
                    db_type="sqlite",
                    connection=SqlalchemyConnection(
                        url=f"sqlite:///{path_enum.path_sqlite}",
                    ),
                    schemas=[
                        Schema(
                            name=None,
                            table_filter=TableFilter(
                                include=[],
                                exclude=[],
                            ),
                        ),
                    ],
                )
            ],
        )

    @cached_property
    def ohmy_sql_adapter(self: "One") -> Adapter:
        return Adapter(
            config=self.ohmy_sql_config,
        )

    @strands.tool
    def list_databases(
        self,
    ):
        return self.ohmy_sql_adapter.tool_list_databases()

    @strands.tool
    def list_tables(
        self,
        database_identifier: str,
        schema_name: T.Optional[str] = None,
    ):
        return self.ohmy_sql_adapter.tool_list_tables(
            database_identifier=database_identifier,
            schema_name=schema_name,
        )

    @strands.tool
    def get_all_database_details(
        self,
    ):
        return self.ohmy_sql_adapter.tool_get_all_database_details()

    @strands.tool
    def get_schema_details(
        self,
        database_identifier: str,
        schema_name: T.Optional[str] = None,
    ):
        return self.ohmy_sql_adapter.tool_get_schema_details(
            database_identifier=database_identifier,
            schema_name=schema_name,
        )

    @strands.tool
    def execute_select_statement(
        self,
        database_identifier: str,
        sql: str,
        params: T.Optional[dict[str, T.Any]] = None,
    ):
        return self.ohmy_sql_adapter.tool_execute_select_statement(
            database_identifier=database_identifier,
            sql=sql,
            params=params,
        )
