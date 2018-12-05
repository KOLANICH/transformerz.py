import typing
import ast
from warnings import warn

from ..core import FileTransformerBase


class PythonASTSerializer(FileTransformerBase):
	__slots__ = ("blacken", "autopep")
	tgtType = ast.AST
	srcType = str

	def __init__(self, name: str, blacken: bool = True, autopep: bool = True) -> None:
		super().__init__(name, "py", "text/x-python")
		self.blacken = blacken
		self.autopep = autopep

	def unprocess(self, v: tgtType) -> srcType:  # pylint:disable=undefined-variable
		import astor  # pylint:disable=import-outside-toplevel

		source = astor.to_source(v, indent_with="\t")

		if self.autopep:
			try:
				import autopep8  # pylint:disable=import-outside-toplevel

				source = autopep8.fix_code(source, options={"max_line_length": 100500, "aggressive": 4, "experimental": True})
			except ImportError:
				warn("Installing `autopep8` may improve results style.")
			except BaseException as ex:
				warn("Error during autopeping. " + repr(ex))

		if self.blacken:
			try:
				import black  # pylint:disable=import-outside-toplevel

				source = black.format_str(source, mode=black.Mode(line_length=100500))
			except ImportError:
				warn("Installing `black` may improve results style.")
			except BaseException as ex:
				warn("Error during blackening. " + repr(ex))

		return source

	def process(self, v: typing.Union[srcType]) -> tgtType:  # pylint:disable=undefined-variable
		return ast.parse(v)


pythonASTSerializer = PythonASTSerializer("pythonAST", False, False)
pythonASTFancySerializer = PythonASTSerializer("pythonAST", True, True)
