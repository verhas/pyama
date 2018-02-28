from pyama.segmenthandler import SegmentHandler
from pyama.file import Segment
import re
import logging

snippets = {}

logger = logging.getLogger(__name__)


class SnippetReader(SegmentHandler):
    start_line = 'START\\s+SNIPPET\\s+(\\w[\\w\\d_]*)'

    def passes(self):
        '''
        :return: snippets are read into memory in the first round and then they are not read any more
        '''
        return [1]

    def start(self):
        return SnippetReader.start_line

    def end(self):
        return 'END\\s+SNIPPET'

    def handle(self, pass_nr, segment: Segment):
        startline = segment.text[0]
        if not re.search(SnippetReader.start_line, startline):
            return
        if segment.filename not in snippets:
            snippets[segment.filename] = {}
        if segment.name not in snippets[segment.filename]:
            logger.debug("Starting snippet %s" % segment.name)
            snippets[segment.filename][segment.name] = segment.text
        else:
            # concatenating snippets remove the start line from the appended snippet and the end line from the
            # already stored snippet
            logger.debug("Continuing snippet %s" % segment.name)
            snippets[segment.filename][segment.name] = snippets[segment.filename][segment.name][:-1] + segment.text[1:]


class SnippetWriter(SegmentHandler):
    # (.{0}) will match a zero length name, and thus the segment will be numbered. We do not need a name, this is an
    # out out segment.
    start_line = 'USE\\s+SNIPPET(.{0})\\s+([\\w\\d_/\\.\\*]+)'

    def passes(self):
        '''
        :return: snippet references are modified when all snippets are already in memory
        '''
        return [2]

    def start(self):
        return SnippetWriter.start_line

    def end(self):
        return '//\\s*END\\s+SNIPPET'

    def _get_modified_text(self, snippet_reference):
        match = re.search("(.*)/(\\w[\\w\\d_]*)", snippet_reference)
        if not match:
            logger.warning("'%s' reference is not file/name format" % snippet_reference)
        file = match.group(1)
        snippet = match.group(2)
        return self._get_snippet_text(file, snippet)

    def _get_snippet_text(self, file, snippet):
        if file == '*':
            text = self.find_joker_snippet(snippet)
        else:
            text = file in snippets and snippet in snippets[file] and snippets[file][snippet]
            if not text:
                logger.warning("snippet %s/%s is not defined" % (file, snippet))
            logger.debug("snippet %s/%s is %s" % (file, snippet, text))
        return text

    def find_joker_snippet(self, snippet):
        found_nr = 0
        text = False
        for k, v in snippets.items():
            found = snippet in v and v[snippet]
            if found:
                if text:
                    text = text[:-1] + found[1:]
                else:
                    text = found
                found_nr += 1
        if found_nr == 0:
            logger.warning("undefined snippet %s is used" % snippet)
        if found_nr > 1:
            logger.warning("used snippet %s is defined in multiple files" % snippet)
        return text

    # START SNIPPET SnippetWriter_handle
    def handle(self, pass_nr, segment):
        startline = segment.text[0]
        match = re.search(SnippetWriter.start_line, startline)
        if not match:
            return
        text = self._get_modified_text(match.group(2))
        if not text:
            return
        segment.text = [segment.text[0]] + text[1:-1] + [segment.text[-1]]
        segment.modified = True
    # END SNIPPET


class MdSnippetWriter(SnippetWriter):
    """
    Markdown Snippet writer is a bit modified snippet writer. When replacing snippet with the modified text
    the ``` line has to be kept after the snippet start line. Also the end of the snippet is signalled by the
    ``` characters and there is no need for any extra END SNIPPET kind of line.
    """

    def end(self):
        return '```\\s*\n'

    # START SNIPPET MdSnippetWriter_handle
    def handle(self, pass_nr, segment: Segment):
        if not re.search(".*\\.md$", segment.filename):
            return
        startline = segment.text[0]
        match = re.search(SnippetWriter.start_line, startline)
        if not match:
            return
        text = self._get_modified_text(match.group(2))
        if not text:
            return
        if len(segment.text) < 2:
            logger.warning("segment %s/%s is too short, can not be processed" % (segment.filename,segment.name))
        else:
            segment.text = [segment.text[0], segment.text[1]] + \
                           text[1:-1] + \
                           [segment.text[-1]]
            segment.modified = True
    # END SNIPPET
