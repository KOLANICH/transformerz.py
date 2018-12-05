import typing
import struct

from .core import TransformerBase


class StructTransformer(TransformerBase):
	__slots__ = ("struct",)
	srcType = bytes
	tgtType = tuple

	def __init__(self, name: str) -> None:
		self.struct = struct.Struct(name)
		super().__init__(name)

	def unprocess(self, v: typing.Any) -> srcType:  # pylint:disable=undefined-variable
		return self.struct.pack(*v)

	def process(self, v: typing.Union[srcType, bytearray, "lmdb.memoryview"]) -> typing.Any:
		return self.struct.unpack(v)


class IntTransformer(StructTransformer):
	__slots__ = ("tgtType",)

	def __init__(self, name: str, tgtType: type):
		self.tgtType = tgtType
		super().__init__(name)

	def unprocess(self, v: typing.Any) -> StructTransformer.srcType:  # pylint:disable=undefined-variable
		return super().unprocess((v,))

	def process(self, v: typing.Union[StructTransformer.srcType, bytearray, "lmdb.memoryview"]) -> typing.Any:
		return super().process(v)[0]


int64Transformer = IntTransformer("=q", int)


class uint64(int):
	pass


uint64Transformer = IntTransformer("=Q", uint64)
