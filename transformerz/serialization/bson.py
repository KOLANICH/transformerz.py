__all__ = ("bsonSerializer", "bsonSerializableTypes")
from ..core import FileTransformer

from bson import BSON  # pymongo


bsonSerializableTypes = (list, dict)
bsonSerializer = FileTransformer("bson", BSON.encode, BSON.decode, bytes, bsonSerializableTypes, "json", "application/json")
