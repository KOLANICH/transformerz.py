import typing

from .core import TransformerMirroringTgtType


class DummyTransformer(TransformerMirroringTgtType):
	"""Does nothing"""

	__slots__ = ("tgtType",)

	def __init__(self, name: str, tgtType: type) -> None:
		self.tgtType = tgtType
		super().__init__(name)

	def unprocess(self, v: typing.Any) -> typing.Any:
		return v

	def process(self, v: typing.Any) -> typing.Any:
		return v


dummyTransformer = DummyTransformer("dummy", object)
