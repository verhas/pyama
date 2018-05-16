#! /usr/bin/python
# -*- coding: utf8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# START SNIPPET run_py
from pyama.configuration import Configuration
from pyama.lineskipperhandler import LineSkipper
from pyama.processor import Processor
from pyama.regexhandler import RegexHandler
from pyama.shellsnippet import ShellSnippet
from pyama.snippet import MdSnippetWriter, SnippetReader, SnippetMacro

snippetWriter = MdSnippetWriter()
# SNIPPET SKIP AFTER '"""\)'
snippetWriter.no_warning("""
WARNING:pyama.snippet:undefined snippet whatever_my_snippet is used
WARNING:pyama.snippet:snippet */whatever_my_snippet is not defined
WARNING:pyama.snippet:snippet filename/snippetname is not defined
WARNING:pyama.snippet:snippet filename/snippetname is not defined
WARNING:pyama.snippet:snippet doc/snippet.md/xetters is not defined
WARNING:pyama.snippet:snippet pyama.py/run__py is not defined
WARNING:pyama.snippet:undefined snippet license_handler is used
WARNING:pyama.snippet:snippet */license_handler is not defined
""")
MD = Configuration().file(r".*\.md$").handler(snippetWriter, SnippetReader(), LineSkipper())
SEGMENT = Configuration().file(r".*\.md$").exclude(r"regexhandler\.md").handler(RegexHandler())
PY = Configuration().file(r".*\.py$").handler(SnippetReader(), ShellSnippet())
JAVA = Configuration().file(r".*\.java$").handler(SnippetReader(), SnippetMacro())
configs = [MD, PY, JAVA, SEGMENT]

Processor(configs, "**/*.*").process()
# END SNIPPET

"""
EXECUTE FOR SNIPPET run_output
python3
pyama.py
-h
END SNIPPET 
"""
