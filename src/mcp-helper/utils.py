# -*- coding: utf-8 -*-
import oss2
import os
from pathlib import Path
import logging

LOGGER = logging.getLogger()


# BUCKET_NAME = "mcp-fc-{}".format(os.environ["FC_REGION"])
BUCKET_NAME = os.environ["BUCKET_NAME"]
auth = oss2.StsAuth(
    os.environ["ALIBABA_CLOUD_ACCESS_KEY_ID"],
    os.environ["ALIBABA_CLOUD_ACCESS_KEY_SECRET"],
    os.environ["ALIBABA_CLOUD_SECURITY_TOKEN"],
)

REGION = os.environ["FC_REGION"]
endpoint = "https://oss-{}.aliyuncs.com".format(REGION)
bucket = oss2.Bucket(auth, endpoint, BUCKET_NAME, region=REGION)


def get_bin(path, package_name):
    directory = Path(path)
    if directory.exists() and directory.is_dir():
        files = [item.name for item in directory.iterdir() if item.is_file()]
        if files:
            if len(files) == 1:
                LOGGER.info(f"Unique executable filename: {files[0]}")
                return files[0]
            else:
                LOGGER.info(f"{files}, {package_name}")
                targetFile = None
                li = package_name.split("/")
                p = li[-1]
                LOGGER.info(li[-1])
                if "@" in li[-1]:
                    pli = li[-1].split("@")
                    p = pli[0]
                elif "==" in li[-1]:
                    pli = li[-1].split("==")
                    p = pli[0]
                LOGGER.info(p)
                if p:
                    for f in files:
                        if p in f:
                            targetFile = f
                            break
                return targetFile

        else:
            LOGGER.info("The directory is empty; there are no files.")
    else:
        LOGGER.info(
            f"Directory '{directory}' does not exist or is not a valid directory."
        )
    raise Exception("Could not find the bin executable file")
