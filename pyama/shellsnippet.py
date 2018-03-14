import logging
import re
import subprocess
import sys

from pyama.segmenthandler import SegmentHandler
from pyama.snippet import store_snippet

logger = logging.getLogger(__name__)


class ShellSnippet(SegmentHandler):
    start_line = r'EXECUTE FOR SNIPPET\s+(\w[\w\d_]*)'

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
        if not re.search(ShellSnippet.start_line, segment.text[0]):
            return
        if sys.platform.startswith("win"):
            exec = ["cmd.exe", "/C"]
        else:
            exec = []
        for line in segment.text[1:-1]:
            exec.append(line.rstrip())
        try:
            text = subprocess.check_output(exec, shell=False).decode("utf-8")
            text = re.split("(\n)",text)
            store_snippet(segment.filename, segment.name, segment.text[0:1] + text + [segment.text[-1]])
        except:
            logger.error("Can not execute '%s'" % ' '.join(exec))
