import os.path
import re
from glob import glob

from pyama.segmenthandler import SegmentHandler
from pyama.snippet import store_data_snippet


class Directory:
    def __init__(self):
        self.sub = None
        self.type = None


class GlobHandler(SegmentHandler):
    """
    List the files in a directory structure and create textual representation into the segment
    """

    def __init__(self, runpass=[1]):
        self.my_glob = glob  # for test mocking only
        self.isfile = os.path.isfile  # for test mocking only
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
        if not re.search(r'\bGLOB\b', segment.text[0]):
            return
        pattern = segment.parameter('PATTERN') or '*.*'
        recursive = segment.parameter('RECURSIVE') == "TRUE"
        name = segment.parameters['NAME']
        files = self.my_glob(pattern, recursive=recursive)
        data = Directory()
        data.sub = {}
        data.type = "dir"
        for file in files:
            path = file.split("/")
            current = data
            for dir in path[:-1]:
                if dir not in current.sub:
                    f = Directory()
                    f.sub = {}
                    f.type = "dir"
                    current.sub[dir] = f
                current = current.sub[dir]
            f = Directory()
            f.type = "file" if self.isfile(file) else "dir"
            file_name = path[-1]
            current.sub[file_name] = f

        store_data_snippet(segment.filename, name, segment.text, data, glob_formatter)


directory_indent = 2


def append_single_name(name, text, level, lines):
    if lines and level > 1:
        text.append(("{:>" + "%s" % (level - 2) + "s}|-{}\n").format('', name))
    else:
        text.append(("{:>" + "%s" % level + "s}{}\n").format('', name))


def tree(dirs, level=0, text=None, lines=False, dir_only=False):
    text = [] if not text else text
    if not dir_only:
        for name in dirs.sub:
            dir = dirs.sub[name]
            if dir.type == "file":
                append_single_name(name, text, level, lines)
    for name in dirs.sub:
        dir = dirs.sub[name]
        if dir.type == "dir":
            append_single_name(name, text, level, lines)
            if dir.sub:
                tree(dir, level + directory_indent, text, lines=lines, dir_only=dir_only)
    return text


def glob_formatter(snippet, segment):
    lines = segment.parameter("LINES") == "TRUE"
    dir_only = segment.parameter("DIRONLY") == "TRUE"
    return snippet.text[:1] + tree(snippet.data, lines=lines, dir_only=dir_only) + snippet.text[-1:]
