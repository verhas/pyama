#! /usr/bin/python
# -*- coding: utf8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# START SNIPPET run_py
from pyama.configuration import Configuration
from pyama.processor import Processor
from pyama.shellsnippet import ShellSnippet
from pyama.snippet import MdSnippetWriter, SnippetReader, SnippetMacro

snippetWriter = MdSnippetWriter()
# SNIPPET SKIP TILL "^MD"
snippetWriter.no_warning("""
WARNING:pyama.snippet:snippet filename/snippetname is not defined
WARNING:pyama.snippet:snippet filename/snippetname is not defined
WARNING:pyama.snippet:snippet doc/snippet.md/xetters is not defined
WARNING:pyama.snippet:undefined snippet license_handler is used
WARNING:pyama.snippet:snippet */license_handler is not defined
WARNING:pyama.snippet:snippet run.py/run__py is not defined
WARNING:pyama.snippet:undefined snippet whatever_my_snippet is used
WARNING:pyama.snippet:snippet */whatever_my_snippet is not defined
""")
MD = Configuration().file(r".*\.md$").handler(snippetWriter, SnippetReader())
PY = Configuration().file(r".*\.py$").handler(SnippetReader(), ShellSnippet())
JAVA = Configuration().file(r".*\.java$").handler(SnippetReader(), SnippetMacro())
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
