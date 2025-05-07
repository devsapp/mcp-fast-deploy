# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from typing import Dict, Any, List


class Client:
    """
    This is a map module
    """

    def __init__(self):
        pass

    @staticmethod
    def size(
        raw: Dict[str, Any],
    ) -> int:
        return len(raw)

    @staticmethod
    def key_set(
        raw: Dict[str, Any],
    ) -> List[str]:
        return list(raw.keys())
