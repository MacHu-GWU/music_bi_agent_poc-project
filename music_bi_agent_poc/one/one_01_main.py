# -*- coding: utf-8 -*-

from .one_02_aws import AwsMixin
from .one_03_agent import AgentMixin
from .one_04_sql import SqlMixin


class One(
    AwsMixin,
    AgentMixin,
    SqlMixin,
):
    pass


one = One()

from ..utils import get_description

one.list_databases.tool_spec["description"] = get_description(one.ohmy_sql_adapter.tool_list_databases)
one.list_tables.tool_spec["description"] = get_description(one.ohmy_sql_adapter.tool_list_tables)
one.get_all_database_details.tool_spec["description"] = get_description(one.ohmy_sql_adapter.tool_get_all_database_details)
one.get_schema_details.tool_spec["description"] = get_description(one.ohmy_sql_adapter.tool_get_schema_details)
one.execute_select_statement.tool_spec["description"] = get_description(one.ohmy_sql_adapter.tool_execute_select_statement)
