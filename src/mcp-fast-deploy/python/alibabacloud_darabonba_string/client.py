# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.


class Client(object):
    """
    This is a string module
    """

    @staticmethod
    def split(raw, sep, limit):
        return raw.split(sep, -1 if limit is None else limit - 1)

    @staticmethod
    def replace(raw, old_str, new_str, count):
        return raw.replace(old_str, new_str, -1 if count is None else count)

    @staticmethod
    def contains(s, sub_str):
        return sub_str in s

    @staticmethod
    def count(s, sub_str):
        return s.count(sub_str)

    @staticmethod
    def has_prefix(s, prefix):
        return s.startswith(prefix)

    @staticmethod
    def has_suffix(s, sub_str):
        return s.endswith(sub_str)

    @staticmethod
    def index(s, sub_str):
        try:
            return s.index(sub_str)
        except ValueError:
            return -1

    @staticmethod
    def to_lower(s):
        return s.lower()

    @staticmethod
    def to_upper(s):
        return s.upper()

    @staticmethod
    def sub_string(s, start, end):
        return s[start:end]

    @staticmethod
    def equals(expect, actual):
        return expect == actual

    @staticmethod
    def trim(raw):
        return raw.strip()

    @staticmethod
    def to_bytes(raw, encoding):
        return raw.encode(encoding)
