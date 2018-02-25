#! /usr/bin/python
# -*- coding: utf8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import unittest

from pyama.collector import FileCollector


class TestFileCollector(unittest.TestCase):
    def testCollectsFiles(self):
        for file in FileCollector("../pyama/**/*.*").collect():
            print(file)


if __name__ == '__main__':
    unittest.main()
