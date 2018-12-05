import typing
from types import FunctionType
import struct

from ..kaitai.compress import KaitaiCompressor, KaitaiProcessor
from .TransformersRegistry import registry


class _TransformerBase:
	__slots__ = ()
	tgtType = None
	srcType = None
	registry = registry

	def __init__(self, name: str) -> None:
		raise NotImplementedError

	def __repr__(self):
		return self.__class__.__name__ + "<>"

	def __add__(self, another):
		res = TransformerStack(self)
		res.extend(another)
		return res

	def __radd__(self, another):
		res = TransformerStack(self)
		res.rextend(another)
		return res


class TransformerStack(_TransformerBase):
	__slots__ = ("_stack", "_id")

	def __init__(self, stack=None) -> None:
		self._id = None
		if stack is None:
			stack = ()
		elif isinstance(stack, TransformerStack):
			stack = type(stack._stack)(stack._stack)
		elif isinstance(stack, _TransformerBase):
			stack = (stack,)
		else:
			stack = list(self.__class__._flatten(stack))

		self._stack = stack

	@property
	def tgtType(self):
		return self._stack[-1].tgtType

	@property
	def srcType(self):
		return self._stack[0].srcType

	@classmethod
	def _getInvalidPairs(cls, chain):
		"""Verifies valdity of the chain"""
		try:
			it = iter(chain)
			prevT = next(it)
		except StopIteration:
			return ()

		for i, t in enumerate(it):
			if prevT.tgtType != t.srcType:
				yield i, prevT, t

	def validate(self):
		return tuple(self.__class__._getInvalidPairs(self._stack))

	@classmethod
	def _generateId(cls, stack) -> typing.Tuple[str]:
		return tuple((t.id for t in stack))

	@property
	def id(self):
		if self._id is None:
			self._id = self.__class__._generateId(self._stack)
		return self._id

	def __bool__(self):
		return bool(self._stack)

	def __len__(self):
		return len(self._stack)

	@classmethod
	def _flatten(cls, extension: typing.Iterable[_TransformerBase]):
		for t in extension:
			if isinstance(t, __class__):
				yield from cls._flatten(t)
			else:
				yield t

	def _extend(self, extension: typing.Union[typing.Iterable[_TransformerBase], _TransformerBase]):
		idExtension = None
		if isinstance(extension, __class__):
			extension = extension._stack
			if self._id is not None:
				idExtension = extension._id
		elif isinstance(extension, _TransformerBase):
			idExtension = (extension.id,)
			extension = (extension,)
		else:
			extension = tuple(self.__class__._flatten(extension))

		if idExtension is None and self._id is not None:
			idExtension = self.__class__._generateId(extension)
		return extension, idExtension

	def extend(self, extension: typing.Iterable[_TransformerBase]):
		extension, idExtension = self._extend(extension)
		self._stack += extension
		if self._id is not None:
			self._id += idExtension

	def rextend(self, extension: typing.Iterable[_TransformerBase]):
		extension, idExtension = self._extend(extension)
		self._stack = extension + self._stack
		if self._id is not None:
			self._id = idExtension + self._id

	def __iadd__(self, another):
		if isinstance(another, TransformerStack):
			self.extend(another)
		else:
			self.extend((another,))
		return self

	def __iter__(self):
		yield from self._stack

	def __getitem__(self, k):
		return self._stack[k]

	def __repr__(self):
		return self.__class__.__name__ + "<" + repr(self._stack) + ">"

	def process(self, data):  # pylint:disable=undefined-variable
		for transformer in self._stack:
			prevRes = data
			#sys.stdout.write("?"+"<= "+repr(data)+"<= "+transformer.id)
			data = transformer.process(data)
			#sys.stdout.write("\b")
			#print(repr(data), "<=", repr(prevRes))
		#print("\n")
		return data

	def unprocess(self, data):  # pylint:disable=undefined-variable
		transformers = reversed(self._stack)
		transformers = list(transformers)
		for transformer in transformers:
			#sys.stdout.write(repr(data) + " => " + transformer.id)
			data = transformer.unprocess(data)
			#sys.stdout.write(" => " + repr(data) + "\n")
		#print("\n")
		return data


class TransformerBase(_TransformerBase):
	__slots__ = ("id",)

	def __init__(self, name: str) -> None:
		self.id = name
		if self.__class__.registry and name not in registry:
			self.__class__.registry.register(self)

	def __repr__(self):
		return self.__class__.__name__ + "<" + self.id + ">"


class FileTransformerBase(TransformerBase):
	__slots__ = ("fileExtension", "mimeType")

	def __init__(self, name: str, fileExtension: str, mimeType: typing.Optional[str] = None) -> None:
		super().__init__(name)
		self.fileExtension = fileExtension
		self.mimeType = mimeType


class TransformerMirroringTgtType(TransformerBase):
	__slots__ = ()

	@property
	def srcType(self) -> type:
		return self.tgtType


class Transformer(TransformerBase):
	__slots__ = ("unprocess", "process", "tgtType", "srcType")

	def __init__(self, name: str, unprocess: FunctionType, process: FunctionType, srcType: type, tgtType: type) -> None:
		self.tgtType = tgtType
		self.srcType = srcType
		self.unprocess = unprocess
		self.process = process
		super().__init__(name)


class FileTransformer(Transformer):
	__slots__ = ("fileExtension", "mimeType")

	def __init__(self, name: str, unprocess: FunctionType, process: FunctionType, srcType: type, tgtType: type, fileExtension: str, mimeType: typing.Optional[str] = None) -> None:
		super().__init__(name, unprocess, process, srcType, tgtType)
		self.fileExtension = fileExtension
		self.mimeType = mimeType
