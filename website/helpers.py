# Helper functions

from base64 import b32decode, b32encode


def id_to_string(id: bytes) -> str:
    return b32encode(id).decode('utf-8').replace("=", "")


def string_to_id(string: str) -> bytes:
    id = None
    while id is None:
        try:
            id = b32decode(string)
        except Exception as e:
            if e.args[0].find("padding") != -1:
                string = f"{string}="
            else:
                raise e
    return id
