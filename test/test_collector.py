#! /usr/bin/python
# -*- coding: utf8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import unittest

from pyama.collector import FileCollector
from pyama.configuration import Configuration


class TestFileCollector(unittest.TestCase):
    def testCollectsFiles(self):
        files = FileCollector([Configuration().file(r"\.snip$")], "**/*.*").collect()
        self.assertEqual(1, len(files), "There is only one *.snip file")
        self.assertEqual("snippet_test.snip", [x for x in files][0], "The file is snippet_test.snip")


if __name__ == '__main__':
    unittest.main()
