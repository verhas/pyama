#! /usr/bin/python
# -*- coding: utf8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# START SNIPPET run_py
from pyama.configuration import Configuration
from pyama.snippet import MdSnippetWriter, SnippetReader
from pyama.processor import Processor


MD = Configuration().file(".*\\.md$").handler(MdSnippetWriter())
PY = Configuration().file(".*\\.py$").handler(SnippetReader())

configs = [MD,PY]
Processor(configs, "**/*.*").process()
# END SNIPPET

