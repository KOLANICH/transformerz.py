import typing
from types import FunctionType

from .kaitai.compress import KaitaiCompressor, KaitaiProcessor
from .core import TransformerBase


class BinaryProcessor(TransformerBase):
	tgtType = bytes
	srcType = bytes
	registry = None

	def __init__(self, name: str, processor: KaitaiProcessor) -> None:
		self.processor = processor
		super().__init__(name)

	def process(self, data: srcType) -> tgtType:  # pylint:disable=undefined-variable
		return self.processor.process(data)(slice(None, None, None))

	def unprocess(self, data: tgtType) -> srcType:  # pylint:disable=undefined-variable
		return self.processor.unprocess(data)(slice(None, None, None))


class BinaryProcessorFactory:
	__slots__ = ("id", "defaultParams", "kaitaiProcessorClass", "defaultProcessor")
	processorClass = BinaryProcessor

	def constructProcessor(self, params: typing.Optional[typing.Dict[str, typing.Any]] = None) -> BinaryProcessor:
		return self.__class__.processorClass(self.id, self.kaitaiProcessorClass(**params))

	def __init__(self, name: str, kaitaiProcessorClass: typing.Type[KaitaiProcessor], defaultParams: dict = None) -> None:
		self.id = name
		if defaultParams is None:
			self.defaultParams = {}
		else:
			self.defaultParams = defaultParams

		self.kaitaiProcessorClass = kaitaiProcessorClass

		self.defaultProcessor = self.constructProcessor({})

	def __call__(self, params: dict = None) -> BinaryProcessor:
		if not params:
			return self.defaultProcessor
		paramsRes = {}
		paramsRes.update(self.defaultParams)
		paramsRes.update(params)
		return self.constructProcessor(paramsRes)
