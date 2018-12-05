__all__ = ("msgpackSerializer",)
from ..core import FileTransformer
from . import jsonSerializableTypes

import msgpack

msgpackPacker = msgpack.Packer(use_bin_type=True, strict_types=True)
msgpackSerializer = FileTransformer("msgpack", msgpackPacker.pack, lambda d: msgpack.unpackb(d, raw=False), bytes, jsonSerializableTypes, "msgpack")
