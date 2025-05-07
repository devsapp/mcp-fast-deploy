# -*- coding: utf-8 -*-

import logging
import subprocess
import json
import os
from pathlib import Path
from utils import bucket, BUCKET_NAME, get_bin

LOGGER = logging.getLogger()

REGION = os.environ["FC_REGION"]
RUNTIME_OS = os.environ["RUNTIME_OS"]


def handler(event, context):
    rid = context.request_id
    working_dir = os.path.join("/tmp", rid)
    os.makedirs(working_dir, exist_ok=True)

    evt = json.loads(event)
    cmd = evt["cmd"].strip()
    if cmd.startswith("uvx"):
        cmd = cmd.replace("uvx", "pip install")
    try:
        cmdLi = cmd.split(" ")
        package_name = cmdLi[2]
        LOGGER.info(f"package_name:  {package_name}")
        cmdLi = [
            "pip",
            "install",
            package_name,
            "-t",
            "python",
            "--ignore-requires-python",
        ]
        if REGION.startswith("cn-") and REGION != "cn-hongkong":
            cmdLi.append("--index-url=https://mirrors.aliyun.com/pypi/simple")
        LOGGER.info(f"cmdLi:  {cmdLi}")
        subprocess.check_call(cmdLi, cwd=working_dir)
        package_file_name = package_name.replace("@", "_").replace("/", "-")
        object_name = f"{package_file_name}_{RUNTIME_OS}.zip"
        # subprocess.check_call(["ls", "-lh"], cwd=working_dir)
        subprocess.check_call(["zip", "-ry", object_name, "."], cwd=working_dir)
        local_file_path = os.path.join(working_dir, object_name)
        bucket.put_object_from_file(object_name, local_file_path)
        bin_path = get_bin(os.path.join(working_dir, "python", "bin"), package_name)

        stdio_cmd = os.path.join("/code/python", "bin", bin_path)
        origin_cmd_li = evt["cmd"].strip().split(" ")
        if len(origin_cmd_li) > 2:
            stdio_cmd += " " + " ".join(origin_cmd_li[2:])

        return {
            "bucket": BUCKET_NAME,
            "object": object_name,
            "start_cmd": [
                "supergateway",
                "--stdio",
                stdio_cmd,
                "--port",
                "8080",
                "--ssePath",
                "/sse",
                "--messagePath",
                "/message",
            ],
        }

    except Exception as e:
        LOGGER.error(e)
        raise e
    finally:
        subprocess.check_call(["rm", "-rf", working_dir])
