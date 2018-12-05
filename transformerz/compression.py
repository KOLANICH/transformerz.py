import typing
from collections import OrderedDict

from .processors import BinaryProcessor, BinaryProcessorFactory
from .kaitai.compress import KaitaiCompressor


class Compressor(BinaryProcessor):
	__slots__ = ()

	def compute_optimal_dict(self, data: typing.Iterable[bytes], dictSize: int = None):
		return self.processor.compute_optimal_dict(data, dictSize)

	@property
	def supportsDicts(self) -> bool:
		return self.processor.__class__.compute_optimal_dict is not KaitaiCompressor.compute_optimal_dict


class BinaryCompressorFactory(BinaryProcessorFactory):
	__slots__ = ()
	processorClass = Compressor


# todo:
# https://github.com/inikep/XWRT
# https://github.com/byronknoll/cmix
# https://github.com/schnaader/precomp-cpp
# https://bellard.org/nncp/


class _compressors:
	__slots__ = ()
	_COMPRESSORS_DICT = None
	_BEST = None


class compressorsMeta(type):
	__slots__ = ()

	def __new__(cls: typing.Type["compressorsMeta"], className: str, parents: tuple, attrs: typing.Dict[str, typing.Any], *args, **kwargs) -> typing.Type["compressors"]:
		compressorsTemp = []

		# pylint:disable=import-outside-toplevel

		try:
			from .kaitai.compress.algorithms.lz4 import Lz4 as KaitaiLz4

			compressorsTemp.append(BinaryCompressorFactory("lz4", KaitaiLz4, {"block_size": None, "compression_level": None}))
		except ImportError:
			pass

		from .kaitai.compress.algorithms.zlib import Zlib as KaitaiZlib, Container as KaitaiZlibContainerType, zlib

		compressorsTemp.append(BinaryCompressorFactory("deflate", KaitaiZlib, {"containerType": KaitaiZlibContainerType.raw, "log_window_size": 15, "level": zlib.Z_BEST_COMPRESSION}))

		try:
			from .kaitai.compress.algorithms.zstd import Zstd as KaitaiZstd

			# FORMAT_ZSTD1_MAGICLESS results in "ZstdError: error determining content size from frame header" because this error is used not only for that. The true error is unknown
			# write_content_size=False results in the same error because content size must be known
			compressorsTemp.append(BinaryCompressorFactory("zstd", KaitaiZstd, {"format": "zstd1", "should_write_uncompressed_size": True, "level": 0, "should_write_dict_id": False, "should_write_checksum": False}))
			#zstd.train_dictionary(dict_size=131072, samples, k=None, d=None, steps=None, threads=None,notifications=0, dict_id=0, level=0)
		except ImportError:
			pass

		try:
			from .kaitai.compress.algorithms.brotli import Brotli as KaitaiBrotli

			compressorsTemp.append(BinaryCompressorFactory("brotli", KaitaiBrotli))
		except ImportError:
			pass

		#try:
		from .kaitai.compress.algorithms.bz2 import Bz2 as KaitaiBz2

		compressorsTemp.append(BinaryCompressorFactory("bzip2", KaitaiBz2))
		#except:
		#	pass

		try:
			from .kaitai.compress.algorithms.lzma import Lzma as KaitaiLzma, lzma

			compressorsTemp.append(BinaryCompressorFactory("lzma", KaitaiLzma, {"format": lzma.FORMAT_RAW, "check": lzma.CHECK_NONE, "additional_filters": [{"id": "delta", "dist": 5}]}))
		except ImportError:
			pass

		#from .kaitai.compress.algorithms.bz2 import KaitaiBz2

		attrsNew = OrderedDict()
		attrsNew["none"] = None

		attrsNew.update((cctor.id, cctor) for cctor in compressorsTemp)

		attrsNew["_COMPRESSORS_DICT"] = type(attrsNew)(attrsNew)
		attrsNew["_BEST"] = compressorsTemp[-1]
		attrsNew.update(attrs)

		return super().__new__(cls, className, parents, attrsNew, *args, **kwargs)


class compressors(_compressors, metaclass=compressorsMeta):
	__slots__ = ()
