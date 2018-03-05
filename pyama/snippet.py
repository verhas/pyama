from pyama.segmenthandler import SegmentHandler
from pyama.file import Segment
import re
import logging
from pyama.template import SnippetFormatter

snippets = {}
macros = {}

logger = logging.getLogger(__name__)


class SnippetMacro(SegmentHandler):
    def __init__(self):
        self.sf = SnippetFormatter()
        self.regex = None

    def set(self, key, value):
        macros[key] = value

    def format(self, text, local):
        return [s + '\n' for s in self.sf.format(''.join(text), **{**macros, **local}).split('\n')][:-1]

    def handle(self, pass_nr, segment):
        if segment.name == "0":
            self.regex = None
        for line in segment.text[1:-1]:
            if re.search("NO\\s+MATCH\\W", line):
                self.regex = None
                continue
            startline = re.search("MATCH\\s+(.*)", line)
            if startline:
                self.regex = startline.group(1)
                continue
            if self.regex:
                match = re.search(self.regex, line)
                if match and match.lastindex >= 2:
                    self.set(match.group(1), match.group(2))


class SnippetReader(SegmentHandler):
    start_line = 'START\\s+SNIPPET\\s+(\\w[\\w\\d_]*)'

    def __init__(self):
        self.macro = SnippetMacro()

    def passes(self):
        '''
        :return: snippets are read into memory in the first round and then they are not read any more
        '''
        return [1]

    def start(self):
        return SnippetReader.start_line

    def end(self):
        return 'END\\s+SNIPPET'

    def fetch_values(self, text, regex):
        for line in text:
            match = re.search(regex, line)
            if match and match.lastindex >= 2:
                self.macroset(match.group(1), match.group(2))

    def handle(self, pass_nr, segment):
        startline = segment.text[0]
        if not re.search(SnippetReader.start_line, startline):
            return
        if segment.filename not in snippets:
            logger.debug("first snippet for file %s" % segment.filename)
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

    def __init__(self):
        self.macro = SnippetMacro()

    def passes(self):
        '''
        :return: snippet references are modified when all snippets are already in memory
        '''
        return [2]

    def start(self):
        return SnippetWriter.start_line

    def end(self):
        return 'END\\s+SNIPPET'

    def _get_modified_text(self, snippet_reference, segment, process=True):
        match = re.search("(.*)/(\\w[\\w\\d_]*)", snippet_reference)
        if not match:
            logger.warning("'%s' reference is not file/name format" % snippet_reference)
            return None
        file = match.group(1)
        snippet = match.group(2)
        return self._get_snippet_text(file, snippet, segment, process)

    def _get_snippet_text(self, file, snippet, segment, process=True):
        if file == '*':
            text = self.find_joker_snippet(snippet)
        else:
            if file == '.':
                file = segment.filename
            text = file in snippets and snippet in snippets[file] and snippets[file][snippet]
        if not text:
            logger.warning("snippet %s/%s is not defined" % (file, snippet))
            return False
        logger.debug("snippet %s/%s is %s" % (file, snippet, text))
        if process:
            return self.processed(text, segment)
        else:
            if re.search("\\s+TEMPLATE\\s+",text[0]):
                logger.warning("snippet was used as parameter, will not be processed as template: %s" % text[0][0:-1])
            return text

    def processed(self, text, segment):
        line = text[0]
        if not re.search("\\s+TEMPLATE\\s+", line):
            if re.search("\\s+WITH\\s+", segment.text[0]):
                logger.warning("Using non-template snippet with parameters: %s" % segment.text[0])
            return text
        line = segment.text[0]
        try:
            if re.search("\\s+WITH\\s+", line):
                local = self.get_local_parameters(line, segment)
                return self.macro.format(text, local)
            return self.macro.format(text, {})
        except KeyError as ke:
            logger.warning(
                "snippet macros were not processed for %s in file %s" % (segment.text[0][:-1], segment.filename))
            logger.warning("Key %s is missing" % ke)
            return text

    def get_local_parameters(self, line, segment):
        local = {}
        match = re.search("\\s+WITH\\s+(.*)$", line)
        line = match.group(1)
        while len(line) > 0:
            value_is_from_snippet = False
            match = re.search("(\\w[\\w\\d_]*)\\s*=\\s*\"(.*?)\"\\s*(.*)$", line)
            if not match:
                match = re.search("(\\w[\\w\\d_]*)\\s*=\\s*'(.*?)'\\s*(.*)$", line)
            if not match:
                match = re.search("(\\w[\\w\\d_]*)\\s*->\\s*(?:'|\")(.*?)(?:'|\")\\s*(.*)$", line)
                value_is_from_snippet = True
            if match:
                line = match.group(3)
                if value_is_from_snippet:
                    text = self._get_modified_text(match.group(2), segment, process=False)
                    text = self.chomp(text)
                    value = "".join(text[1:-1])
                else:
                    value = match.group(2)
                local[match.group(1)] = value
            else:
                break
        return local

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

    def chomp(self, text, inline=True):
        """remove the last \n if the segment is to be chomped"""
        if not re.search("TRUNCATE", text[0]):
            return text
        if len(text) < 2:
            logger.warning("segment %s is too short to trunace the last line " % text[0])
        if text[-2][-1] == '\n' and text[-2][-2] == '\\':
            chomped = [s for s in text]
            if inline:
                chomped[-2] = chomped[-2][0:-2]
            else:
                chomped[-2] = chomped[-2][0:-2] + '\n'
            return chomped
        else:
            return text

    # START SNIPPET SnippetWriter_handle
    def handle(self, pass_nr, segment):
        startline = segment.text[0]
        match = re.search(SnippetWriter.start_line, startline)
        if not match:
            return
        text = self._get_modified_text(match.group(2), segment)
        if not text:
            return
        text = self.chomp(text,False)
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
        return '```\\s*\n|END\\s+SNIPPET'

    # START SNIPPET MdSnippetWriter_handle
    def handle(self, pass_nr, segment: Segment):
        if not re.search(".*\\.md$", segment.filename):
            return
        startline = segment.text[0]
        match = re.search(SnippetWriter.start_line, startline)
        if not match:
            return
        text = self._get_modified_text(match.group(2), segment)
        if not text:
            return
        if len(segment.text) < 2:
            logger.warning("segment %s/%s is too short, can not be processed" % (segment.filename, segment.name))
        else:
            text = self.chomp(text,False)
            segment.text = [segment.text[0], segment.text[1]] + \
                           text[1:-1] + \
                           [segment.text[-1]]
            segment.modified = True
    # END SNIPPET
