from pyama.segmenthandler import SegmentHandler
from pyama.file import Segment
import re

snippets = {}


class SnippetReader(SegmentHandler):
    start_line = '//\\s*START\\s+SNIPPET\\s+(\\w[\\w\\d_]*)'

    def passes(self):
        '''
        :return: snippets are read into memory in the first round and then they are not read any more
        '''
        return [1]

    def start(self):
        return SnippetReader.start_line

    def end(self):
        return '//\\s*END\\s+SNIPPET'

    def handle(self, pass_nr, segment: Segment):
        startline = segment.text[0]
        if re.search(SnippetReader.start_line, startline):
            if segment.filename not in snippets:
                snippets[segment.filename] = {}
            if segment.name not in snippets[segment.filename]:
                snippets[segment.filename][segment.name] = []

            snippets[segment.filename][segment.name] += segment.text


class SnippetWriter(SegmentHandler):
    # (.{0}) will match a zero length name, and thus the segment will be numbered. We do not need a name, this is an
    # out out segment.
    start_line = '//\\s*USE\\s+SNIPPET(.{0})\\s+(.*)'

    def passes(self):
        '''
        :return: snippet references are modified when all snippets are already in memory
        '''
        return [2]

    def start(self):
        return SnippetWriter.start_line

    def end(self):
        return '//\\s*END\\s+SNIPPET'

    def handle(self, pass_nr, segment: Segment):
        startline = segment.text[0]
        match = re.search(SnippetWriter.start_line, startline)
        if match:
            snippet_reference = match.group(2)
            match = re.search("(.*)/(\\w[\\w\\d_]*)", snippet_reference)
            if not match:
                print("ERROR: '%s' reference is not file/name format" % snippet_reference)
            file = match.group(1)
            snippet = match.group(2)
            if file == '*':
                for k,v in snippets.items():
                    text = snippet in v and v[snippet]
                    if text:
                        break
            else:
                text = file in snippets and snippet in snippets[file] and snippets[file][snippet]
            if text:
                segment.text = [segment.text[0]] + text[1:len(text)-1] + [segment.text[len(segment.text) - 1]]
