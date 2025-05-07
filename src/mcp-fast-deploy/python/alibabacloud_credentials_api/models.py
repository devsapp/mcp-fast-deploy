# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.


class ICredentials:
    def get_access_key_id(self) -> str:
        raise NotImplementedError("get_access_key_id() must be overridden")

    def get_access_key_secret(self) -> str:
        raise NotImplementedError("get_access_key_secret() must be overridden")

    def get_security_token(self) -> str:
        raise NotImplementedError("get_security_token() must be overridden")

    def get_provider_name(self) -> str:
        raise NotImplementedError("get_provider_name() must be overridden")


class ICredentialsProvider:
    def get_credentials(self) -> ICredentials:
        raise NotImplementedError("get_credentials() must be overridden")

    async def get_credentials_async(self) -> ICredentials:
        raise NotImplementedError("get_credentials_async() must be overridden")

    def get_provider_name(self) -> str:
        raise NotImplementedError("get_provider_name() must be overridden")
