import logging
import re
import subprocess
import sys

from pyama.segmenthandler import SegmentHandler
from pyama.snippet import store_snippet
from pyama.regex_helper import re_search

logger = logging.getLogger(__name__)


class ShellHander(SegmentHandler):
    def init_exec(self):
        if sys.platform.startswith("win"):
            return ["cmd.exe", "/C"]
        else:
            return []

    def execute(self, exec):
        try:
            text = subprocess.check_output(exec, shell=False).decode("utf-8")
            return re.split("(\n)", text.replace('\r', ''))
        except:
            logger.error("Can not execute '%s'" % ' '.join(exec))
            return None


class ShellSnippet(ShellHander):
    start_line = r'EXECUTE\s+FOR\s+SNIPPET\s+(\w[\w\d_]*)'

    def passes(self):
        '''
        :return: snippets are read into memory in the first round and then they are not read any more
        '''
        return [1]

    def start(self):
        return ShellSnippet.start_line

    def end(self):
        return r'END\s+SNIPPET'

    def handle(self, pass_nr, segment):
        if not re_search(ShellSnippet.start_line, segment.text[0]):
            return

        exec = self.init_exec()

        for line in segment.text[1:-1]: exec.append(line.rstrip())

        text = self.execute(exec)
        if text: store_snippet(segment.filename, segment.name, segment.text[0:1] + text + [segment.text[-1]])
