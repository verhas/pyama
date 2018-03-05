#! /usr/bin/python
# -*- coding: utf8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import unittest

from pyama.configuration import Configuration
from pyama.snippet import SnippetWriter, SnippetReader, SnippetMacro
from pyama.snippet import reset as snippetreset
from pyama.processor import Processor
from test.testsupport import copy_template, TARGET, assertEqual
from glob import glob


class TestSnippets(unittest.TestCase):

    def test_simple_snippet_use(self):
        for file in glob("test_templates/*.tmpl"):
            file = file.replace("\\", "/").replace(".tmpl", "").replace("test_templates/", "")
            self.process_single_file(file)

    def test_complex_templating(self):
        TEST = "template_complex"
        copy_template(TEST,template_ext=".tmpl_x")
        TXT = Configuration() \
            .file(TARGET + TEST + ".txt") \
            .handler(SnippetReader(), SnippetWriter(), SnippetMacro())
        configs = [TXT]
        processor = Processor(configs, TARGET + TEST + ".txt")
        macro = SnippetMacro()
        macro.set("name", "Peter Verhas")
        processor.process()
        assertEqual(TEST)
        snippetreset()

    def process_single_file(self, TEST):
        copy_template(TEST)
        TXT = Configuration() \
            .file(TARGET + TEST + ".txt") \
            .handler(SnippetReader(), SnippetWriter(), SnippetMacro())
        configs = [TXT]
        processor = Processor(configs, TARGET + TEST + ".txt")
        processor.process()
        assertEqual(TEST)
        snippetreset()


if __name__ == '__main__':
    unittest.main()
