# -*- coding: utf-8 -*-

"""
Usage:

    from common.log import logger

    logger.info("test")
    logger.error("wrong1")
    logger.exception("wrong2")

    # with traceback
    try:
        1 / 0
    except Exception:
        logger.exception("wrong3")
"""

import logging

util_logger = logging.getLogger("root")
component_logger = logging.getLogger('component')
