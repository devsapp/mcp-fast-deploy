# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
import hmac
import hashlib
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key

from .sm3 import Sm3


class Signer:
    """
    Signature Util for Darabonba.
    """

    def __init__(self):
        pass

    @staticmethod
    def hmac_sha1sign(
        string_to_sign: str,
        secret: str,
    ) -> bytes:
        """
        HmacSHA1 Signature
        @param string_to_sign: string
        @param secret: string
        @return: signed bytes
        """
        return Signer.hmac_sha1sign_by_bytes(string_to_sign, secret.encode("utf-8"))

    @staticmethod
    def hmac_sha1sign_by_bytes(
        string_to_sign: str,
        secret: bytes,
    ) -> bytes:
        """
        HmacSHA1 Signature
        @param string_to_sign: string
        @param secret: bytes
        @return: signed bytes
        """
        string_to_sign = string_to_sign.encode("utf-8")
        return hmac.new(secret, string_to_sign, digestmod=hashlib.sha1).digest()

    @staticmethod
    def hmac_sha256sign(
        string_to_sign: str,
        secret: str,
    ) -> bytes:
        """
        HmacSHA256 Signature
        @param string_to_sign: string
        @param secret: string
        @return: signed bytes
        """
        return Signer.hmac_sha256sign_by_bytes(string_to_sign, secret.encode("utf-8"))

    @staticmethod
    def hmac_sha256sign_by_bytes(
        string_to_sign: str,
        secret: bytes,
    ) -> bytes:
        """
        HmacSHA256 Signature
        @param string_to_sign: string
        @param secret: bytes
        @return: signed bytes
        """
        string_to_sign = string_to_sign.encode("utf-8")
        return hmac.new(secret, string_to_sign, hashlib.sha256).digest()

    @staticmethod
    def hmac_sm3sign(
        string_to_sign: str,
        secret: str,
    ) -> bytes:
        """
        HmacSM3 Signature
        @param string_to_sign: string
        @param secret: string
        @return: signed bytes
        """
        return Signer.hmac_sm3sign_by_bytes(string_to_sign, secret.encode("utf-8"))

    @staticmethod
    def hmac_sm3sign_by_bytes(
        string_to_sign: str,
        secret: bytes,
    ) -> bytes:
        """
        HmacSM3 Signature
        @param string_to_sign: string
        @param secret: bytes
        @return: signed bytes
        """
        string_to_sign = string_to_sign.encode("utf-8")
        return hmac.new(secret, string_to_sign, Sm3).digest()

    @staticmethod
    def sha256with_rsasign(
        string_to_sign: str,
        secret: str,
    ) -> bytes:
        """
        SHA256withRSA Signature
        @param string_to_sign: string
        @param secret: string
        @return: signed bytes
        """
        string_to_sign = string_to_sign.encode("utf-8")
        secret = secret.encode("utf-8")
        if not secret.startswith(b"-----BEGIN RSA PRIVATE KEY-----"):
            secret = b"-----BEGIN RSA PRIVATE KEY-----\n%s" % secret
        if not secret.endswith(b"-----END RSA PRIVATE KEY-----"):
            secret = b"%s\n-----END RSA PRIVATE KEY-----" % secret

        key = load_pem_private_key(secret, password=None, backend=default_backend())
        return key.sign(string_to_sign, padding.PKCS1v15(), hashes.SHA256())

    @staticmethod
    def md5sign(
        string_to_sign: str,
    ) -> bytes:
        """
        MD5 Signature
        @param string_to_sign: string
        @return: signed bytes
        """
        return Signer().md5sign_for_bytes(string_to_sign.encode("utf-8"))

    @staticmethod
    def md5sign_for_bytes(
        bytes_to_sign: bytes,
    ) -> bytes:
        """
        MD5 Signature
        @param string_to_sign: string
        @return: signed bytes
        """
        return hashlib.md5(bytes_to_sign).digest()
