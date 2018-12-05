#!/usr/bin/env python3
import typing
import random
import sqlite3
import sys
import unittest
import warnings
from functools import partial
from pathlib import Path
import random
import sqlite3
import unittest

thisDir = Path(__file__).parent.absolute()
sys.path.insert(0, str(thisDir.parent))


def testString():
	return "Aa12Бб_" + str(random.randint(1, 0xFFFFFFFF))  # nosec


class SimpleTests(unittest.TestCase):
	pass


if __name__ == "__main__":
	unittest.main()
