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

    def test_inner_properties(self):
        schema = load("inner_properties")
        Ioo = build_class(schema)
        ioo = Ioo()
        self.assertRaises(TypeError, setattr, ioo, "inner", ioo.getclass("inner"))
        self.assertRaises(TypeError, setattr, ioo, "outer", ioo.getclass("outer"))
        ioo.outer = ioo.getclass("outer")()
        self.assertRaises(ConstraintError, setattr, ioo.outer, "string", "123Ciao")
        setattr(ioo.outer, "string", "v:2.3.4")
        self.assertEqual(ioo.outer.string, "v:2.3.4")

    def test_basic_array(self):
        schema = load("basic_array")
        barray = build_class(schema)()
        barray.array = []
        self.assertEqual(barray.array, [])
        self.assertRaises(TypeError, setattr, barray, "array", ["INVALID_VALUE"])
        self.assertRaises(TypeError, setattr, barray, "array", [23, 45, "INVALID_VALUE", 12])
        barray.array = [24]
        self.assertEqual(barray.array, [24])
        self.assertRaises(ConstraintError, setattr, barray, "array", [12])

    def test_variant(self):
        schema = load("variant_schema")
        variant = build_class(schema)()
        self.assertEqual(variant.avprop, [])
        with self.assertRaises(TypeError):
            variant.avprop = ["Hello"]
        variant.avprop = [variant.getclass("avprop")[0]()]
        with self.assertRaises(TypeError):
            variant.vprop = "Hello"
        variant.vprop = variant.getclass("vprop")[0]()
