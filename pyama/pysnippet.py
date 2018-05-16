import logging
import sys
from io import StringIO

from pyama.regex_helper import re_search
from pyama.segmenthandler import SegmentHandler
from pyama.snippet import store_snippet

logger = logging.getLogger(__name__)

snippet_globals_dict = dict()


class PySnippet(SegmentHandler):
    start_line = r'PYTHON\s+SNIPPET\s+(\w[\w\d_]*)'

    def passes(self):
        '''
        :return: snippets are read into memory in the first round and then they are not read any more
        '''
        return [1]

    def start(self):
        return PySnippet.start_line

    def end(self):
        return r'END\s+SNIPPET'

    def handle(self, pass_nr, segment):
        match = re_search(PySnippet.start_line, segment.text[0])
        if not match:
            return
        globals_name = segment.parameter("GLOBALS")
        if not globals_name:
            globals_name = "_"
        if globals_name:
            if globals_name == "*":
                snippet_globals = globals()
            else:
                if globals_name not in snippet_globals_dict:
                    snippet_globals_dict[globals_name] = dict()
                snippet_globals = snippet_globals_dict[globals_name]

        code_out = StringIO()
        code_err = StringIO()

        code = ''
        for line in segment.text[1:-1]:
            code = code + line
        sysstdout = sys.stdout
        sysstderr = sys.stderr
        # capture output and errors
        sys.stdout = code_out
        sys.stderr = code_err

        try:
            exec(code, snippet_globals)
        except Exception as e:
            logger.error("Python snippet threw up")
            logger.error(e)

        # restore stdout and stderr
        sys.stdout = sysstdout
        sys.stderr = sysstderr

        s = code_err.getvalue()
        if len(s) > 0:
            logger.error("Python snippet is erroneous")
            logger.error(s)

        text = code_out.getvalue()
        store_snippet(segment.filename, segment.name, segment.text[0:1] + [text] + [segment.text[-1]])
        code_out.close()
        code_err.close()
