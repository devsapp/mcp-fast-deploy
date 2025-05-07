# -*- coding: utf-8 -*-

import logging
import subprocess
import json
import os
from pathlib import Path
from utils import bucket, BUCKET_NAME, get_bin

REGION = os.environ["FC_REGION"]
RUNTIME_OS = os.environ["RUNTIME_OS"]

LOGGER = logging.getLogger()


def handler(event, context):
    LOGGER.info(event)

    rid = context.request_id
    working_dir = os.path.join("/tmp", rid)
    os.makedirs(working_dir, exist_ok=True)
    with open(os.path.join(working_dir, "package.json"), "w", encoding="utf-8") as file:
        file.write("{}")

    evt = json.loads(event)
    cmd = evt["cmd"].strip()
    if cmd.startswith("npx -y"):
        cmd = cmd.replace("npx -y", "npm install")
    try:
        cmdLi = cmd.split(" ")
        package_name = cmdLi[2]
        LOGGER.info(f"package_name:  {package_name}")
        if REGION.startswith("cn-") and REGION != "cn-hongkong":
            cmdLi.append("--registry=https://registry.npmmirror.com")
        LOGGER.info(f"cmdLi:  {cmdLi}")
        subprocess.check_call(cmdLi, cwd=working_dir)

        package_file_name = package_name.replace("@", "_").replace("/", "-")
        object_name = f"{package_file_name}_{RUNTIME_OS}.zip"
        # subprocess.check_call(["ls", "-lh"], cwd=working_dir)
        subprocess.check_call(["zip", "-ry", object_name, "."], cwd=working_dir)
        local_file_path = os.path.join(working_dir, object_name)
        bucket.put_object_from_file(object_name, local_file_path)
        bin_path = get_bin(
            os.path.join(working_dir, "node_modules", ".bin"), package_name
        )

        stdio_cmd = os.path.join("/code/node_modules", ".bin", bin_path)
        origin_cmd_li = evt["cmd"].strip().split(" ")
        if len(origin_cmd_li) > 3:
            stdio_cmd += " " + " ".join(origin_cmd_li[3:])

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
