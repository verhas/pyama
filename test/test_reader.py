#! /usr/bin/python
# -*- coding: utf8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import unittest

from pyama.filereader import FileReader


class TestFileReader(unittest.TestCase):
    def testReadsFile(self):
        reader = FileReader(
            "sample_reader_test.txt",
            regexes=[('name="(\\w+)"','END SEGMENT'),
                     ('\\s*\\*\\s*START\\s*(\\w+)','END SEGMENT'),
                     ("PYTHON\s+SEGMENT\s+(\\w[\\w\\d_]*)",None)]
            )
        file = reader.read()
        for segment in file.segments:
            print("... segment '%s'" % segment.name)
            print(">>>%s<<<" % "".join(segment.text))

if __name__ == '__main__':
    unittest.main()
