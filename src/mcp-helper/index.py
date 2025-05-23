# -*- coding: utf-8 -*-

import logging
import json
from pathlib import Path
import npx
import uvx
from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class CustomRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        request_id = self.headers.get("x-fc-request-id", "unknown")
        print("FC Invoke Start RequestId: " + request_id)
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8")

        logger = logging.getLogger()
        logger.info(body)

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        evt = json.loads(body)
        cmd = evt["cmd"].strip()
        if cmd.startswith("npx"):
            ret = npx.handler(body, request_id)
        elif cmd.startswith("uvx"):
            ret = uvx.handler(body, request_id)
        else:
            raise Exception("cmd not support")
        self.wfile.write(json.dumps(ret).encode("utf-8"))
        print("FC Invoke End RequestId: " + request_id)


if __name__ == "__main__":
    server_address = ("", 8000)
    httpd = HTTPServer(server_address, CustomRequestHandler)
    print("Server running on port 8000...")
    httpd.serve_forever()
