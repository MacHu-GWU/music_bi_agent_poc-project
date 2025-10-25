# -*- coding: utf-8 -*-

import typing as T
from functools import cached_property

from boto_session_manager import BotoSesManager
import strands

if T.TYPE_CHECKING:  # pragma: no cover
    from .one_01_main import One


class AwsMixin:
    @cached_property
    def bsm(self: "One") -> BotoSesManager:
        return BotoSesManager(profile_name="esc_app_dev_us_east_1")

    @cached_property
    def model(self: "One") -> strands.models.BedrockModel:
        return strands.models.BedrockModel(
            # model_id="us.amazon.nova-pro-v1:0",
            model_id="us.amazon.nova-lite-v1:0",
            boto_session=self.bsm.boto_ses,
        )
