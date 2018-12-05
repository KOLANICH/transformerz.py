import typing

from .core import TransformerBase


class EncodingTransformer(TransformerBase):
	__slots__ = ()
	tgtType = str
	srcType = bytes

	def __init__(self, name: str) -> None:
		super().__init__(name)

	def unprocess(self, v: tgtType) -> srcType:  # pylint:disable=undefined-variable
		return v.encode(self.id)

	def process(self, v: typing.Union[srcType, bytearray, "lmdb.memoryview"]) -> tgtType:  # pylint:disable=undefined-variable
		return str(v, encoding=self.id)  # memoryview has no `decode`


utf8Transformer = EncodingTransformer("utf-8")
