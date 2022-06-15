# Helper functions

from base64 import b32decode, b32encode, b64encode
from website.models import Cuisine
from . import db


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


def get_cuisine(name: str):
    cuisine = Cuisine.query.filter_by(name=name).first()
    if cuisine is None:
        cuisine = Cuisine(name=name)
        db.session.add(cuisine)
        db.session.commit()
    return cuisine


def b64(b):
    return b64encode(b).decode()
