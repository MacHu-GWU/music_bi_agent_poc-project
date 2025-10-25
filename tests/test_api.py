# -*- coding: utf-8 -*-

from music_bi_agent_poc import api


def test():
    _ = api


if __name__ == "__main__":
    from music_bi_agent_poc.tests import run_cov_test

    run_cov_test(
        __file__,
        "music_bi_agent_poc.api",
        preview=False,
    )
