__all__ = ("cborSerializer",)
from ..core import FileTransformer
from . import jsonSerializableTypes


try:
	import cbor
except ImportError:
	import cbor2 as cbor
cborSerializer = FileTransformer("cbor", cbor.dumps, cbor.loads, bytes, jsonSerializableTypes, "cbor")
