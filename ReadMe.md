transformerz.py [![Unlicensed work](https://raw.githubusercontent.com/unlicense/unlicense.org/master/static/favicon.png)](https://unlicense.org/)
===============
[wheel (from GHA via `nightly.link`)](https://nightly.link/KOLANICH-libs/transformerz.py/workflows/CI/master/transformerz-0.CI-py3-none-any.whl)
![GitLab Build Status](https://gitlab.com/KOLANICH/transformerz.py/badges/master/pipeline.svg)
[![GitHub Actions](https://github.com/KOLANICH-libs/transformerz.py/workflows/CI/badge.svg)](https://github.com/KOLANICH-libs/transformerz.py/actions)
![GitLab Coverage](https://gitlab.com/KOLANICH/transformerz.py/badges/master/coverage.svg)
[![Coveralls Coverage](https://img.shields.io/coveralls/KOLANICH/transformerz.py.svg)](https://coveralls.io/r/KOLANICH/transformerz.py)
[![Libraries.io Status](https://img.shields.io/librariesio/github/KOLANICH-libs/transformerz.py.svg)](https://libraries.io/github/KOLANICH-libs/transformerz.py)

Just a set of composable processor objects that can be stacked, and path can be automatically routed.

Each class/object has 2 members of type `type`:

* `tgtType`
* `srcType`

and 2 functions

* `process` - converts a value of `srcType` to the `tgtType`. Should parse the data from the representation useful for storing on disk.
* `unprocess` - converts a value of  `tgtType` to `srcType` Should serialize the data from the representation useful for storing on disk.
.

The names of functions are inherited from `kaitai.process` library (Kaitai Struct is a parsing framework, so `process` historically means parsing), so are some classes (and I hope to get the stuff from this package merged supported by KS somewhen).

There are 3 base classes:

* `TransformerBase` - for objects with `srcType` and `tgtType` hardcoded in class definitions or available as props
* `Transformer` - for objects with `srcType` and `tgtType` stored in slots
* `FileTransformer` - for transformations when `unprocess`ed form can be stored in a file with a well-known extension and possible MIME type.
* `BinaryProcessor` - adapter for Kaitai Struct stuff


There are transformers are of different types and reside in different submodules:

* `.serialization` - packages to serialize various objects
	* `.json.jsonSerializer` -  Uses `ujson` if it is available which is faster than built-in `json` module.
	* `.bson.bsonSerializer` - Available if `pymongo` is installed.
	* `.msgpack.msgpackSerializer` - Available if a package for MsgPack serialization is installed.
	* `.cbor.cborSerializer` - Available packages for CBOR serialization: either `cbor` or `cbor2` - are installed.
	* `.pon.ponSerializer` - "Python Object Nonation" - stuff like JSON that can be safely evaluated using `literal_eval`
* `.processors` - process binary data. This module contains the adapters allowing to use the stuff written to be used in `process` attr in Kaitai Struct specs.
* `.compression` - packages to compress binary data. Take various params.
* `.text` - convert text to bytes and back
* `.struct` - parses data to tuples and back using `struct.Struct`. Numbers binary representations also go here. But not all. Some cannot be parsed by `struct`, so they go to ...
* `.numpy` - parsing and serializing arrays of numbers using `numpy` machinery. Mostly needed for IEEE 751 floats not built into python.

Tutorial
--------

The tutorial is available. [`tutorial.ipynb`](./tutorial.ipynb) ([NBViewer](https://nbviewer.jupyter.org/github/KOLANICH-libs/transformerz.py/blob/master/tutorial.ipynb))
