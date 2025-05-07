# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from urllib.parse import urlencode, quote
import binascii
import hashlib
import base64

from .sm3 import hash_sm3


class Encoder:
    """
    Encode Util for Darabonba.
    """

    def __init__(self):
        pass

    @staticmethod
    def url_encode(
        url: str,
    ) -> str:
        """
        Encode the URL
        @param url: string
        @return: encoded string
        """
        return urlencode(url)

    @staticmethod
    def percent_encode(
        raw: str,
    ) -> str:
        """
        Special encoding for url params.
        @param params: string
        @return: encoded string
        """
        return quote(raw, safe="~", encoding="utf-8")

    @staticmethod
    def path_encode(
        path: str,
    ) -> str:
        """
        Encode the partial path of url.
        @param path: string
        @return: encoded string
        """
        return quote(path, safe="/~", encoding="utf-8")

    @staticmethod
    def hex_encode(
        raw: bytes,
    ) -> str:
        """
        Hex encode for byte array.
        @param raw: byte array
        @return: encoded string
        """
        return binascii.b2a_hex(raw).decode("utf-8")

    @staticmethod
    def hash(
        raw: bytes,
        signature_algorithm: str,
    ) -> bytes:
        """
        Hash the raw data with signatureAlgorithm.
        @param raw: hashing data
        @param signature_algorithm: the autograph method
        @return: hashed bytes
        """
        if "HMAC-SHA256" in signature_algorithm or "RSA-SHA256" in signature_algorithm:
            return hashlib.sha256(raw).digest()
        elif "HMAC-SM3" in signature_algorithm:
            return hash_sm3(raw)

    @staticmethod
    def base_64encode_to_string(
        raw: bytes,
    ) -> str:
        """
        Base64 encoder for byte array.
        @param raw: byte array
        @return: encoded string
        """
        return str(base64.b64encode(raw), encoding="utf-8")

    @staticmethod
    def base_64decode(
        src: str,
    ) -> bytes:
        """
        Base64 dncoder for string.
        @param src: string
        @return: dncoded byte array
        """
        return base64.b64encode(src).decode("utf-8")
