#! /usr/bin/python
# -*- coding: utf8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import unittest

from pyama.file import Segment
from pyama.regexhandler import RegexHandler


class TestRegexHandler(unittest.TestCase):

    def test_replaces_kills_last(self):
        segment = Segment("name", "filename")
        segment.text = ['''        REPLACE "(t)his" -> "\\1hat" 'que(s)tion' -> 'an\\1wer' KILL "k+"\n''',
                        'this is the question\n',
                        'kill this line\n',
                        "END SEGMENT\n"]
        handler = RegexHandler()
        handler.handle(3, segment)
        self.assertEqual("""        REPLACE "(t)his" -> "\\1hat" 'que(s)tion' -> 'an\\1wer' KILL "k+"\n"""
                         """that is the answer\n"""
                         """END SEGMENT\n""", "".join(segment.text))

    def test_replaces_kills_first(self):
        segment = Segment("name", "filename")
        segment.text = ['''        REPLACE "(t)his" -> "\\1hat" 'que(s)tion' -> 'an\\1wer' KILL "k+"\n''',
                        'kill this line\n',
                        'this is the question\n',
                        "END SEGMENT\n"]
        handler = RegexHandler()
        handler.handle(3, segment)
        self.assertEqual("""        REPLACE "(t)his" -> "\\1hat" 'que(s)tion' -> 'an\\1wer' KILL "k+"\n"""
                         """that is the answer\n"""
                         """END SEGMENT\n""", "".join(segment.text))

    def test_replaces_kills_multiple(self):
        segment = Segment("name", "filename")
        segment.text = ['''        REPLACE "(t)his" -> "\\1hat" 'que(s)tion\\n' -> 'an\\1wer' KILL "k+"\n''',
                        'kill this line\n',
                        'kill this line\n',
                        'kill this line\n',
                        'kill this line\n',
                        'kill this line\n',
                        'this is the question\n',
                        'kill this line\n',
                        "END SEGMENT\n"]
        handler = RegexHandler()
        handler.handle(3, segment)
        self.assertEqual("""        REPLACE "(t)his" -> "\\1hat" 'que(s)tion\\n' -> 'an\\1wer' KILL "k+"\n"""
                         """that is the answer\n"""
                         """END SEGMENT\n""", "".join(segment.text))

    def test_replaces_no_kills(self):
        segment = Segment("name", "filename")
        segment.text = ['''        REPLACE "(t)his" -> "\\1hat" 'que(s)tion\\n' -> 'an\\1wer'\n''',
                        'this is the question\n',
                        "END SEGMENT\n"]
        handler = RegexHandler()
        handler.handle(3, segment)
        self.assertEqual("""        REPLACE "(t)his" -> "\\1hat" 'que(s)tion\\n' -> 'an\\1wer'\n"""
                         """that is the answer\n"""
                         """END SEGMENT\n""", "".join(segment.text))

    def test_no_replaces_kills(self):
        segment = Segment("name", "filename")
        segment.text = ['''        REPLACE KILL "k+" \n''',
                        'this is the question\n',
                        "END SEGMENT\n"]
        handler = RegexHandler()
        handler.handle(3, segment)
        self.assertEqual('''        REPLACE KILL "k+" \n'''
                         'this is the question\n'
                         """END SEGMENT\n""", "".join(segment.text))

    def test_no_replaces_no_kills(self):
        segment = Segment("name", "filename")
        segment.text = [''' JUST NOTHING HERE \n''',
                        'this is the question\n',
                        "END SEGMENT\n"]
        handler = RegexHandler()
        handler.handle(3, segment)
        self.assertEqual(''' JUST NOTHING HERE \n'''
                         'this is the question\n'
                         """END SEGMENT\n""", "".join(segment.text))

if __name__ == '__main__':
    unittest.main()
