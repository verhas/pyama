#! /usr/bin/python
# -*- coding: utf8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import unittest

from pyama.filereader import FileReader,Segment


class TestFileReader(unittest.TestCase):
    def test_reads_file(self):
        reader = FileReader(
            "sample_reader_test.txt",
            regexes=[(r'name="(\w+)"', 'END SEGMENT'),
                     (r'\s*\*\s*START\s*(\w+)', 'END SEGMENT'),
                     (r"PYTHON\s+SEGMENT\s+(\w[\w\d_]*)", None)]
        )
        file = reader.read()
        self.assertEqual(7, len(file.segments))
        self.assertEqual('0', file.segments[0].name)
        self.assertEqual(2, len(file.segments[0].text))
        self.assertEqual('segmentOne', file.segments[1].name)
        self.assertEqual(3, len(file.segments[1].text))
        self.assertEqual('1', file.segments[2].name)
        self.assertEqual(1, len(file.segments[2].text))
        self.assertEqual('anotherSegment', file.segments[3].name)
        self.assertEqual(6, len(file.segments[3].text))
        self.assertEqual('2', file.segments[4].name)
        self.assertEqual(2, len(file.segments[4].text))
        self.assertEqual('python_segment', file.segments[5].name)
        self.assertEqual(4, len(file.segments[5].text))
        self.assertEqual('python_segment', file.segments[6].name)
        self.assertEqual(3, len(file.segments[6].text))

    def test_analyses_parameters(self):
        segment = Segment("name","file name")
        line = """ SNIPPET START A=B B=13 K='ha mi' ZIG="ZA G" WITH hami -> "mami"   """
        FileReader("whatnot",["onces"]).analyze_parameters(line,segment)
        self.assertEqual(segment.parameters["A"],"B")
        self.assertEqual(segment.parameters["B"],"13")
        self.assertEqual(segment.parameters["K"],"ha mi")
        self.assertEqual(segment.parameters["ZIG"],"ZA G")

if __name__ == '__main__':
    unittest.main()
