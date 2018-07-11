import json
import unittest
from os.path import join

TEST_BASE = "schemas/"


def load(file):
    with open(join(TEST_BASE, file + ".json"), "r") as reader:
        return json.loads(reader.read())


class Test(unittest.TestCase):
    def test_basicproperties(self):
        pass
