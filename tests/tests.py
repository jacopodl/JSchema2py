import json
import unittest
from os.path import join

from jschema2py import build_class
from jschema2py.constraints import ConstraintError

TEST_BASE = "schemas/"


def load(file):
    with open(join(TEST_BASE, file + ".json"), "r") as reader:
        return json.loads(reader.read())


class Test(unittest.TestCase):
    def test_basicproperties(self):
        schema = load("basic_properties")
        bs = build_class(schema)()
        self.assertEqual(bs.string, "HelloWorld")
        bs.string = "hello"
        self.assertEqual(bs.string, "hello")
        bs.number = .123

    def test_number_schema(self):
        schema = load("number_properties")
        nt = build_class(schema)()
        self.assertRaisesRegex(ConstraintError, "minimum acceptable value: \d", setattr, nt, "min", 2)
        self.assertRaisesRegex(ConstraintError, "maximum acceptable value: \d", setattr, nt, "max", 11)
        self.assertRaisesRegex(ConstraintError, "value must be between \d and \d", setattr, nt, "between", 23)
