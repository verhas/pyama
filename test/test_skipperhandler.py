#! /usr/bin/python
# -*- coding: utf8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import unittest

from pyama.file import Segment
from pyama.lineskipperhandler import LineSkipper


class TestRegexHandler(unittest.TestCase):

    def test_skip_remove(self):
        segment = Segment("name", "filename")
        segment.text = [''' SKIPPER REMOVE\n''',
                        'this stays\n',
                        'this stays\n',
                        ' SNIPPET SKIP 1 LINE\n',
                        'this goes away\n',
                        'this goes away\n',
                        'this goes away\n',
                        'this stays\n',
                        'this stays\n',
                        'this stays\n',
                        'this stays\n',
                        "END SEGMENT\n"]
        handler = LineSkipper()
        handler.handle(3, segment)
        self.assertEqual(''' SKIPPER REMOVE\n'''
                         'this stays\n'
                         'this stays\n'
                         'this goes away\n'
                         'this goes away\n'
                         'this goes away\n'
                         'this stays\n'
                         'this stays\n'
                         'this stays\n'
                         'this stays\n'
                         "END SEGMENT\n", "".join(segment.text))

    def test_skip_1_line(self):
        segment = Segment("name", "filename")
        segment.text = [''' SKIPPER \n''',
                        'this stays\n',
                        'this stays\n',
                        ' SNIPPET SKIP 1 LINE\n',
                        'this goes away\n',
                        'this goes away\n',
                        'this goes away\n',
                        'this stays\n',
                        'this stays\n',
                        'this stays\n',
                        'this stays\n',
                        "END SEGMENT\n"]
        handler = LineSkipper()
        handler.handle(3, segment)
        self.assertEqual(''' SKIPPER \n'''
                         'this stays\n'
                         'this stays\n'
                         'this goes away\n'
                         'this goes away\n'
                         'this stays\n'
                         'this stays\n'
                         'this stays\n'
                         'this stays\n'
                         "END SEGMENT\n", "".join(segment.text))

    def test_skip_lines(self):
        segment = Segment("name", "filename")
        segment.text = [''' SKIPPER \n''',
                        'this stays\n',
                        'this stays\n',
                        ' SNIPPET SKIP 3 LINES\n',
                        'this goes away\n',
                        'this goes away\n',
                        'this goes away\n',
                        'this stays\n',
                        'this stays\n',
                        'this stays\n',
                        'this stays\n',
                        "END SEGMENT\n"]
        handler = LineSkipper()
        handler.handle(3, segment)
        self.assertEqual(''' SKIPPER \n'''
                         'this stays\n'
                         'this stays\n'
                         'this stays\n'
                         'this stays\n'
                         'this stays\n'
                         'this stays\n'
                         "END SEGMENT\n", "".join(segment.text))

    def test_skip_after(self):
        segment = Segment("name", "filename")
        segment.text = [''' SKIPPER \n''',
                        'this stays\n',
                        'this stays\n',
                        ' SNIPPET SKIP AFTER "this stays"\n',
                        'this goes away\n',
                        'this goes away\n',
                        'this goes away\n',
                        'this stays\n',
                        'this stays\n',
                        'this stays\n',
                        'this stays\n',
                        "END SEGMENT\n"]
        handler = LineSkipper()
        handler.handle(3, segment)
        self.assertEqual(''' SKIPPER \n'''
                         'this stays\n'
                         'this stays\n'
                         'this stays\n'
                         'this stays\n'
                         'this stays\n'
                         "END SEGMENT\n", "".join(segment.text))

    def test_skip_till(self):
        segment = Segment("name", "filename")
        segment.text = [''' SKIPPER \n''',
                        'this stays\n',
                        'this stays\n',
                        ' SNIPPET SKIP TILL "this stays"\n',
                        'this goes away\n',
                        'this goes away\n',
                        'this goes away\n',
                        'this stays\n',
                        'this stays\n',
                        'this stays\n',
                        'this stays\n',
                        "END SEGMENT\n"]
        handler = LineSkipper()
        handler.handle(3, segment)
        self.assertEqual(''' SKIPPER \n'''
                         'this stays\n'
                         'this stays\n'
                         'this stays\n'
                         'this stays\n'
                         'this stays\n'
                         'this stays\n'
                         "END SEGMENT\n", "".join(segment.text))

    def test_no_skipper(self):
        segment = Segment("name", "filename")
        segment.text = [''' JUST NOTHING HERE \n''',
                        'this is the question\n',
                        "END SEGMENT\n"]
        handler = LineSkipper()
        handler.handle(3, segment)
        self.assertEqual(''' JUST NOTHING HERE \n'''
                         'this is the question\n'
                         """END SEGMENT\n""", "".join(segment.text))


if __name__ == '__main__':
    unittest.main()
