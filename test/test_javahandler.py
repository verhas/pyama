#! /usr/bin/python
# -*- coding: utf8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import unittest
from glob import glob

from pyama.configuration import Configuration
from pyama.javahandler import JavaHandler
from pyama.licensehandler import LicenseHandler
from pyama.processor import Processor
from test.testsupport import copy_template, TARGET, assertEqual


class TestJavahandler(unittest.TestCase):

    def test_java_generators(self):
        for file in glob("test_templates/*.java_x"):
            file = file.replace("\\", "/").replace(".java_x", "").replace("test_templates/", "")
            self.process_single_file(file)

    def process_single_file(self, TEST):
        license_handler = LicenseHandler()
        license_handler.license("LICENSE.txt")
        copy_template(TEST, ext=".java", template_ext=".java_x")
        JAVA = Configuration() \
            .file(TARGET + TEST + ".java") \
            .handler(JavaHandler(),license_handler)
        configs = [JAVA]
        processor = Processor(configs, TARGET + TEST + ".java")
        processor.process()
        assertEqual(TEST, ext=".java")


if __name__ == '__main__':
    unittest.main()
