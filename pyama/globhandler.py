from glob import glob
import re
from pyama.segmenthandler import SegmentHandler
from pyama.snippet import store_data_snippet


class GlobHandler(SegmentHandler):
    """
    List the files in a directory structure and create textual representation into the segment
    """

    def __init__(self, runpass=[1]):
        self.my_glob = glob
        self.runpass = runpass

    def passes(self):
        '''
        :return: snippet references are modified when all snippets are already in memory
        '''
        return self.runpass

    def start(self):
        return r'\bGLOB\b'

    def end(self):
        return r'\bEND\s+SNIPPET\b'

    def handle(self, pass_nr, segment):
        if not re.search(r'\bGLOB\b',segment.text[0]):
            return
        pattern = segment.parameter('PATTERN') or '*.*'
        recursive = segment.parameter('RECURSIVE') == "TRUE"
        data = self.my_glob(pattern, recursive=recursive)
        store_data_snippet(segment.filename, segment.parameters['NAME'], None, data, glob_formatter)


def glob_formatter(snippet, segment):
    return [s + '\n' for s in snippet.data]
