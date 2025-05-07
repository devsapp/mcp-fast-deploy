# -*- coding: utf-8 -*-
import os
import sys
import json
from typing import List
from alibabacloud_tea_openapi.client import Client as OpenApiClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_fc20230330 import models as fc20230330_models
from alibabacloud_fc20230330.client import Client as FC20230330Client
from alibabacloud_darabonba_stream.client import Client as StreamClient
from io import BytesIO
import uuid
import time

from log import LOGGER

REGION = os.environ["FC_REGION"]
SERVICE_FUNCTION_NAME = os.environ["HELPER_FUNCTION_NAME"]

config = open_api_models.Config(
    access_key_id=os.environ["ALIBABA_CLOUD_ACCESS_KEY_ID"],
    access_key_secret=os.environ["ALIBABA_CLOUD_ACCESS_KEY_SECRET"],
    security_token=os.environ["ALIBABA_CLOUD_SECURITY_TOKEN"],
)
account_id = os.environ["FC_ACCOUNT_ID"]
config.endpoint = f"{account_id}.{REGION}.fc.aliyuncs.com"
config.connect_timeout = 1200000
config.read_timeout = 1200000
client = FC20230330Client(config)


# for example
# cmd = "npx -y @amap/amap-maps-mcp-server"
# envs = {"AMAP_MAPS_API_KEY": os.environ["AMAP_MAPS_API_KEY"]}
async def handler(cmd, envs, name, desc):
    LOGGER.info(
        f"start invoke mcp-helper {cmd}, {envs}, {name}, {SERVICE_FUNCTION_NAME}"
    )
    # body_stream = StreamClient.read_from_string(json.dumps({"cmd": cmd}))
    invoke_function_request = fc20230330_models.InvokeFunctionRequest(
        body=json.dumps({"cmd": cmd}).encode("utf-8")
    )

    start = time.time()
    r = await client.invoke_function_async(
        SERVICE_FUNCTION_NAME, invoke_function_request
    )
    body = r.body

    LOGGER.info(f"mcp-helper time = {time.time()-start}")

    json_dict = {}
    try:
        byte_data = body.getvalue()
        json_str = byte_data.decode("utf-8")
        json_dict = json.loads(json_str)
        LOGGER.info("invoke resp:", json_dict)
    except json.JSONDecodeError as e:
        raise Exception("json decode error")

    finally:
        body.close()

    bucket = json_dict["bucket"]
    object = json_dict["object"]
    start_cmd = json_dict["start_cmd"]
    LOGGER.info(start_cmd)

    # 创建 SSE 函数
    params = open_api_models.Params(
        action="CreateFunction",
        version="2023-03-30",
        protocol="HTTPS",
        method="POST",
        auth_type="AK",
        style="FC",
        pathname=f"/2023-03-30/functions",
        req_body_type="json",
        body_type="json",
    )
    # body params
    function_name = f"{name}_MCP_{uuid.uuid4()}"
    layer = f"acs:fc:{REGION}:1730431480417716:layers/MCP-Runtime-V1/versions/3"
    body = {
        "functionName": function_name,
        "description": desc,
        "cpu": 1,
        "memorySize": 2048,
        "runtime": "custom.debian10",
        "diskSize": 10240,
        "handler": "index.handler",
        "code": {
            "ossBucketName": bucket,
            "ossObjectName": object,
        },
        "instanceConcurrency": 200,
        "timeout": 300,
        "layers": [layer],
        "customRuntimeConfig": {
            "command": start_cmd,
            "port": 8080,
        },
        "sessionAffinity": "MCP_SSE",
        "environmentVariables": {
            "PATH": "/var/fc/lang/python3.10/bin:/var/fc/lang/nodejs20/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/bin:/code/python/bin",
            "FONTCONFIG_FILE": "/opt/etc/fonts.conf",
            "PUPPETEER_EXECUTABLE_PATH": "/opt/google/chrome/chrome",
        },
    }
    if cmd.startswith("npx"):
        body["environmentVariables"].update(
            {"NODE_PATH": "/opt/nodejs/node_modules:/var/fc/lang/nodejs20/node_modules"}
        )
        if REGION.startswith("cn-") and REGION != "cn-hongkong":
            body["environmentVariables"].update(
                {"npm_config_registry": "https://registry.npmmirror.com"}
            )

    if cmd.startswith("uvx"):
        body["environmentVariables"].update({"PYTHONPATH": "/code/python"})
        if REGION.startswith("cn-") and REGION != "cn-hongkong":
            body["environmentVariables"].update(
                {
                    "UV_INDEX_URL": "https://mirrors.aliyun.com/pypi/simple",
                    "UV_PYTHON_INSTALL_MIRROR": "https://mirror.nju.edu.cn/github-release/indygreg/python-build-standalone",
                }
            )

    body["environmentVariables"].update(envs)
    runtime = util_models.RuntimeOptions()
    request = open_api_models.OpenApiRequest(body=body)
    c_f_resp = await client.call_api_async(params, request, runtime)
    LOGGER.info(f"create function status = {c_f_resp}")

    create_trigger_input = fc20230330_models.CreateTriggerInput(
        trigger_type="http",
        trigger_name="http_t",
        trigger_config='{"authType": "anonymous", "methods": ["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"]}',
    )
    # if use auth
    # create_trigger_input = fc20230330_models.CreateTriggerInput(
    #     trigger_type="http",
    #     trigger_name="http_t",
    #     trigger_config="""{"authType": "bearer", "methods": ["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"],
    #         "authConfig": {
    # 		    "bearerFormat": "opaque",
    # 		    "opaqueTokenConfig": {
    #                 "tokens": [
    #                     {
    #                 "tokenName": "my-sk",
    #                 "tokenData": "sk-123456",
    #                 "enable": true
    #                     }
    #                 ]
    # 		    }
    # 		}}""",
    # )
    create_trigger_request = fc20230330_models.CreateTriggerRequest(
        body=create_trigger_input
    )

    c_t_resp = await client.create_trigger_async(function_name, create_trigger_request)
    LOGGER.info(f"create trigger url = {c_t_resp.body.http_trigger.url_internet}")

    return {
        "endpoint": f"{c_t_resp.body.http_trigger.url_internet}/sse",
        "functionArn": c_f_resp["body"]["functionArn"],
    }
