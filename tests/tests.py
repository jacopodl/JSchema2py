import json
import unittest
from os.path import join

from jschema2py import build_class

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
