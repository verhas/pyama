#! /usr/bin/python
# -*- coding: utf8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import unittest

from pyama.configuration import Configuration
from pyama.snippet import SnippetWriter, SnippetReader
from pyama.processor import Processor


class TestProcessor(unittest.TestCase):
    def testProcessing(self):
        TXT = Configuration() \
            .file(".*\\.snip") \
            .handler(SnippetReader(), SnippetWriter())

        configs = [TXT]
        processor = Processor(configs, "../test/*.*")
        processor.process()


if __name__ == '__main__':
    unittest.main()