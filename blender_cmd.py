#!/usr/bin/env python3
"""send commands to blender via the blendermcp socket protocol."""

import socket
import json
import sys

HOST = "localhost"
PORT = 9876


def send_command(cmd_type, params=None):
    """send a command to blender and return the response."""
    payload = {"type": cmd_type}
    if params:
        payload["params"] = params

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(30)
    try:
        sock.connect((HOST, PORT))
        sock.sendall(json.dumps(payload).encode("utf-8"))

        # receive response
        buf = b""
        while True:
            chunk = sock.recv(65536)
            if not chunk:
                break
            buf += chunk
            try:
                result = json.loads(buf.decode("utf-8"))
                return result
            except json.JSONDecodeError:
                continue
    finally:
        sock.close()


def execute_code(code):
    """execute python code in blender."""
    return send_command("execute_code", {"code": code})


def get_scene_info():
    """get current scene info."""
    return send_command("get_scene_info")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        code = " ".join(sys.argv[1:])
        result = execute_code(code)
        print(json.dumps(result, indent=2))
    else:
        result = get_scene_info()
        print(json.dumps(result, indent=2))
