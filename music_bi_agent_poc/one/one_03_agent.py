# -*- coding: utf-8 -*-

import typing as T
from functools import cached_property

import strands

if T.TYPE_CHECKING:  # pragma: no cover
    from .one_01_main import One


class AgentMixin:
    @cached_property
    def router_agent(self: "One") -> strands.Agent:
        return strands.Agent(
            model=self.model,
            # system_prompt=(
            #     ""
            # ),
            # callback_handler=None,
            tools=[],
        )

    @cached_property
    def metrics_agent(self: "One") -> strands.Agent:
        return strands.Agent(
            model=self.model,
            # system_prompt=(
            #     ""
            # ),
            # callback_handler=None,
            tools=[],
        )

    @cached_property
    def sql_agent(self: "One") -> strands.Agent:
        return strands.Agent(
            model=self.model,
            # system_prompt=(
            #     ""
            # ),
            # callback_handler=None,
            tools=[],
        )

    @cached_property
    def knowledge_agent(self: "One") -> strands.Agent:
        return strands.Agent(
            model=self.model,
            # system_prompt=(
            #     ""
            # ),
            # callback_handler=None,
            tools=[],
        )

    @cached_property
    def report_agent(self: "One") -> strands.Agent:
        return strands.Agent(
            model=self.model,
            # system_prompt=(
            #     ""
            # ),
            # callback_handler=None,
            tools=[],
        )
