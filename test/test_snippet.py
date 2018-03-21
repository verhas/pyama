#! /usr/bin/python
# -*- coding: utf8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import unittest
from glob import glob

from pyama.configuration import Configuration
from pyama.linenumberer import LineNumberer
from pyama.lineregexprocessor import LineRegexHandler
from pyama.processor import Processor
from pyama.snippet import SnippetWriter, SnippetReader, SnippetMacro, MdSnippetWriter
from pyama.snippet import reset as snippetreset
from test.testsupport import copy_template, TARGET, assertEqual


class TestSnippets(unittest.TestCase):

    def test_simple_snippetlineregex_use(self):
        for file in glob("test_templates/*.ptmpl"):
            file = file.replace("\\", "/").replace(".ptmpl", "").replace("test_templates/", "")
            self.process_single_processed_use(file)

    def test_simple_snippetlinernumberer_use(self):
        for file in glob("test_templates/*.ntmpl"):
            file = file.replace("\\", "/").replace(".ntmpl", "").replace("test_templates/", "")
            self.process_single_linenumberfile(file)

    def test_simple_md_linernumberer_use(self):
        for file in glob("test_templates/*.md_tmpl"):
            file = file.replace("\\", "/").replace(".md_tmpl", "").replace("test_templates/", "")
            self.process_single_linenumberfile_md(file)

    def test_simple_snippet_use(self):
        for file in glob("test_templates/*.tmpl"):
            file = file.replace("\\", "/").replace(".tmpl", "").replace("test_templates/", "")
            self.process_single_file(file)

    def test_complex_templating(self):
        TEST = "template_complex"
        copy_template(TEST, template_ext=".tmpl_x")
        TXT = Configuration() \
            .file(TARGET + TEST + ".txt") \
            .handler(SnippetReader(), SnippetWriter(), SnippetMacro())
        configs = [TXT]
        processor = Processor(configs, TARGET + TEST + ".txt")
        macro = SnippetMacro()
        macro.set("name", "Peter Verhas")
        macro.set("list", ["A", "B", "C"])
        macro.set("yes", True)
        macro.set("no", False)
        macro.set("dict", {"a": "1", "b": 2, "c": 3})
        processor.process()
        assertEqual(TEST)
        snippetreset()

    def process_single_processed_use(self, TEST):
        copy_template(TEST, ext=".ptxt", template_ext=".ptmpl")
        TXT = Configuration() \
            .file(TARGET + TEST + ".ptxt") \
            .handler(SnippetReader(), SnippetWriter(), LineRegexHandler())
        configs = [TXT]
        processor = Processor(configs, TARGET + TEST + ".ptxt")
        processor.process()
        assertEqual(TEST, ext=".ptxt")
        snippetreset()

    def process_single_linenumberfile_md(self, TEST):
        copy_template(TEST, ext=".md", template_ext=".md_tmpl")
        TXT = Configuration() \
            .file(TARGET + TEST + ".md") \
            .handler(SnippetReader(), MdSnippetWriter(),LineNumberer())
        configs = [TXT]
        processor = Processor(configs, TARGET + TEST + ".md")
        processor.process()
        assertEqual(TEST, ext=".md")
        snippetreset()

    def process_single_linenumberfile(self, TEST):
        copy_template(TEST, ext=".ntxt", template_ext=".ntmpl")
        TXT = Configuration() \
            .file(TARGET + TEST + ".ntxt") \
            .handler(SnippetReader(), SnippetWriter(), LineNumberer())
        configs = [TXT]
        processor = Processor(configs, TARGET + TEST + ".ntxt")
        processor.process()
        assertEqual(TEST, ext=".ntxt")
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
