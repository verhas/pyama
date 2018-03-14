#! /usr/bin/python
# -*- coding: utf8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# START SNIPPET run_py
from pyama.configuration import Configuration
from pyama.snippet import MdSnippetWriter, SnippetReader, SnippetMacro
from pyama.shellsnippet import ShellSnippet
from pyama.processor import Processor

MD = Configuration().file(r".*\.md$").handler(MdSnippetWriter(),SnippetReader())
PY = Configuration().file(r".*\.py$").handler(SnippetReader(), ShellSnippet())
JAVA = Configuration().file(r".*\.java$").handler(SnippetReader(),SnippetMacro())
configs = [MD, PY, JAVA]

Processor(configs, "**/*.*").process()
# END SNIPPET

"""
EXECUTE FOR SNIPPET run_output
python3
run.py
-h
END SNIPPET 
"""
