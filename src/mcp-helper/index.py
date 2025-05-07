# -*- coding: utf-8 -*-

import logging
import json
from pathlib import Path
import npx
import uvx


def handler(event, context):
    logger = logging.getLogger()
    logger.info(event)
    evt = json.loads(event)
    cmd = evt["cmd"].strip()
    if cmd.startswith("npx"):
        return npx.handler(event, context)
    elif cmd.startswith("uvx"):
        return uvx.handler(event, context)
    else:
        raise Exception("cmd not support")
