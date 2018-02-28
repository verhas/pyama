#! /usr/bin/python
# -*- coding: utf8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import unittest

from pyama.configuration import Configuration
from pyama.javahandler import JavaHandler
from pyama.processor import Processor
from pyama.licensehandler import LicenseHandler
import sys

class TestProcessor(unittest.TestCase):
    def testProcessing(self):
        sys.argv = ['test_java.py', '--level','INFO']
        # START SNIPPET license_handler
        licensehandler = LicenseHandler()
        licensehandler.license("LICENSE.txt")
        JAVA = Configuration() \
            .file(".*\\.java") \
            .handler(JavaHandler(),licensehandler)

        configs = [JAVA]
        processor = Processor(configs, "../test/*.java")
        processor.process()
        # END SNIPPET
        self.assertEqual(1, len(processor.files))


if __name__ == '__main__':
    unittest.main()
