#! /usr/bin/python
# -*- coding: utf8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import unittest

from pyama.file import Segment
from pyama.globhandler import GlobHandler


class TestGlobHandler(unittest.TestCase):
    def test_replaces_kills_last(self):
        segment = Segment("name", "filename")
        segment.text = [''' GLOB NAME="file_list"\n''',
                        "END SEGMENT\n",

                        ]
        handler = GlobHandler()
        handler.handle(3, segment)
        self.assertEqual("""        REPLACE "(t)his" -> "\\1hat" 'que(s)tion' -> 'an\\1wer' KILL "k+"\n"""
                         """that is the answer\n"""
                         """END SEGMENT\n""", "".join(segment.text))


if __name__ == '__main__':
    unittest.main()
