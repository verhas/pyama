#! /usr/bin/python
# -*- coding: utf8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# START SNIPPET run_py
from pyama.configuration import Configuration
from pyama.snippet import MdSnippetWriter, SnippetReader, SnippetMacro
from pyama.processor import Processor

MD = Configuration().file(".*\\.md$").handler(MdSnippetWriter(),SnippetReader())
PY = Configuration().file(".*\\.py$").handler(SnippetReader())
JAVA = Configuration().file(".*\\.java$").handler(SnippetReader(),SnippetMacro())
configs = [MD, PY, JAVA]

Processor(configs, "**/*.*").process()
# END SNIPPET
