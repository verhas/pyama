#! /usr/bin/python
# -*- coding: utf8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
from pyama.configuration import Configuration
from pyama.processor import Processor
from pyama.javahandler import JavaHandler
from test.testsupport import copy_template, TARGET, assertEqual
from glob import glob
import unittest


class TestJavahandler(unittest.TestCase):
    def test_java_generators(self):
        for file in glob("test_templates/*.java_x"):
            file = file.replace("\\", "/").replace(".java_x", "").replace("test_templates/", "")
            self.process_single_file(file)

    def process_single_file(self, TEST):
        copy_template(TEST,ext=".java", template_ext=".java_x")
        JAVA = Configuration()\
            .file(TARGET + TEST + ".java") \
            .handler(JavaHandler())
        configs = [JAVA]
        processor = Processor(configs, TARGET + TEST + ".java")
        processor.process()
        assertEqual(TEST,ext=".java")


if __name__ == '__main__':
    unittest.main()
