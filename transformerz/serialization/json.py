__all__ = ("jsonSerializer", "jsonFancySerializer")

import typing
import json as jsonFancy

try:
	import ujson as json
except ImportError:
	json = jsonFancy

from ..core import FileTransformer
from . import jsonSerializableTypes, NoneType

jsonSerializer = FileTransformer("json", json.dumps, json.loads, str, jsonSerializableTypes, "json")


def fancyJSONSerialize(v: typing.Union[jsonSerializableTypes]) -> str:
	return jsonFancy.dumps(v, indent="\t")


jsonFancySerializer = FileTransformer("json", fancyJSONSerialize, json.loads, str, jsonSerializableTypes, "json")
