#! /usr/bin/python
# -*- coding: utf8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import unittest
from glob import glob
import re
from pyama.configuration import Configuration
from pyama.globhandler import GlobHandler
from pyama.linenumberer import LineNumberer
from pyama.processor import Processor
from pyama.regexhandler import RegexHandler
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

    def test_simple_glob(self):
        for file in glob("test_templates/*.gtmpl"):
            file = file.replace("\\", "/").replace(".gtmpl", "").replace("test_templates/", "")
            self.process_glob(file)

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
            .handler(SnippetReader(), SnippetWriter(), RegexHandler(), LineNumberer([4]))
        configs = [TXT]
        processor = Processor(configs, TARGET + TEST + ".ptxt")
        processor.process()
        assertEqual(TEST, ext=".ptxt")
        snippetreset()

    def process_single_linenumberfile_md(self, TEST):
        copy_template(TEST, ext=".md", template_ext=".md_tmpl")
        TXT = Configuration() \
            .file(TARGET + TEST + ".md$") \
            .handler(SnippetReader(), MdSnippetWriter(), LineNumberer())
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

    def process_glob(self, TEST):
        copy_template(TEST, ext=".gtxt", template_ext=".gtmpl")
        glob_handler = GlobHandler()
        glob_handler.my_glob = mock_glob
        glob_handler.isfile = mock_isfile
        TXT = Configuration() \
            .file(TARGET + TEST + ".gtxt") \
            .handler(SnippetReader(), SnippetWriter(), glob_handler)
        configs = [TXT]
        processor = Processor(configs, TARGET + TEST + ".gtxt")
        processor.process()
        assertEqual(TEST, ext=".gtxt")
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


def mock_isfile(file):
    return re.search(r"\.",file)

def mock_glob(pattern, recursive=False):
    if recursive:
        return [
            'sample_reader_test.txt',
            'snippet_test.snip',
            'testsupport.py',
            'test_collector.py',
            'test_filereader.py',
            'test_globhandler.py',
            'test_javahandler.py',
            'test_processor.py',
            'test_regexhandler.py',
            'test_skipperhandler.py',
            'test_snippet.py',
            'test_template.py',
            'subdir/sample_reader_test.txt',
            'subdir/snippet_test.snip',
            'subdir/testsupport.py',
            'subdir/test_collector.py',
            'subdir/test_filereader.py',
            'subdir/test_globhandler.py',
            'subdir/test_javahandler.py',
            'subdir/test_processor.py',
            'subdir/test_regexhandler.py',
            'subdir/test_skipperhandler.py',
            'subdir/test_snippet.py',
            'subdir/test_template.py',
            'subsub/subdir/sample_reader_test.txt',
            'subsub/subdir/snippet_test.snip',
            'subsub/subdir/testsupport.py',
            'subsub/subdir/test_collector.py',
        ]
    else:
        return [
            'sample_reader_test.txt',
            'snippet_test.snip',
            'testsupport.py',
            'test_collector.py',
            'test_filereader.py',
            'test_globhandler.py',
            'test_javahandler.py',
            'test_processor.py',
            'test_regexhandler.py',
            'test_skipperhandler.py',
            'test_snippet.py',
            'test_template.py'
        ]


if __name__ == '__main__':
    unittest.main()
