__all__ = ("ponSerializer", "ponSerializableTypes")

from ast import literal_eval

from ..core import Transformer
from . import jsonSerializableTypes


# "Python Object Notation"

ponSerializableTypes = jsonSerializableTypes + (set, bytes)
ponSerializer = Transformer("pon", repr, literal_eval, str, ponSerializableTypes)
