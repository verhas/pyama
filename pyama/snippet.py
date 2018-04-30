import logging
import re

from pyama.file import Segment
from pyama.regex_helper import re_search
from pyama.segmenthandler import SegmentHandler
from pyama.template import SnippetFormatter

logger = logging.getLogger(__name__)


def reset():
    global snippets, macros
    snippets = {}
    macros = {}


reset()


def get_snippets(file_name):
    if file_name not in snippets:
        logger.debug("first snippet for file %s" % file_name)
        snippets[file_name] = {}
    return snippets[file_name]


def store_snippet(file_name, snippet_name, text):
    store_data_snippet(file_name, snippet_name, text, None, None)


def store_data_snippet(file_name, snippet_name, text, data,formatter):
    file_snippets = get_snippets(file_name)

    if snippet_name not in file_snippets:
        logger.debug("Starting snippet %s" % snippet_name)
        file_snippets[snippet_name] = Snippet()
        file_snippets[snippet_name].text = text
        file_snippets[snippet_name].data = data
        file_snippets[snippet_name].formatter = formatter
    else:
        # concatenating snippets remove the start line from the appended snippet and the end line from the
        # already stored snippet
        logger.debug("Continuing snippet %s/%s" % (file_name, snippet_name))
        if data is not None:
            logger.warning("Snippet %s/%s contains data and can not be continued" % (file_name, snippet_name))
        file_snippets[snippet_name].text = file_snippets[snippet_name].text[:-1] + text[1:]


class Snippet:
    def __init__(self):
        self.text = []
        self.formatter = None
        self.data = None


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
            if re.search(r"NO\s+MATCH\W", line):
                self.regex = None
                continue
            startline = re.search(r"MATCH\s+(.*)", line)
            if startline:
                self.regex = startline.group(1)
                continue
            if self.regex:
                match = re_search(self.regex, line)
                if match and match.lastindex >= 2:
                    self.set(match.group(1), match.group(2))


class SnippetReader(SegmentHandler):
    start_line = r'START\s+SNIPPET\s+(\w[\w\d_]*)'

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
        return r'END\s+SNIPPET'

    def fetch_values(self, text, regex):
        """
        Fetch macro values from the lines of TEXT based on regex
        :param text: the lines that may hold keys and values fr macros
        :param regex: if that matches a line then group(1) is treated as key and group(2) is treated as value and
        stored into the macroset to be references in snippets
        :return:
        """
        for line in text:
            match = re_search(regex, line)
            if match and match.lastindex >= 2:
                self.macroset(match.group(1), match.group(2))

    def handle(self, pass_nr, segment):
        startline = segment.text[0]
        if not re.search(SnippetReader.start_line, startline):
            return
        store_snippet(segment.filename, segment.name, segment.text)


class SnippetWriter(SegmentHandler):
    # (.{0}) will match a zero length name, and thus the segment will be numbered. We do not need a name, this is an
    # out out segment.
    start_line = r'USE\s+SNIPPET(.{0})\s+([\w\d_/\.\*]+)'

    def no_warning(self, string):
        self.warning_exclude = string

    def __init__(self):
        self.macro = SnippetMacro()
        self.warning_exclude = ""

    def passes(self):
        '''
        :return: snippet references are modified when all snippets are already in memory
        '''
        return [2]

    def start(self):
        return SnippetWriter.start_line

    def end(self):
        return r'END\s+SNIPPET'

    def get_modified_text(self, snippet_reference, segment, process=True):
        match = re.search(r"(.*)/(\w[\w\d_]*)", snippet_reference)
        if not match:
            logger.warning("'%s' reference is not file/name format" % snippet_reference)
            return None
        file = match.group(1)
        snippet = match.group(2)
        return self.get_snippet_text(file, snippet, segment, process)

    def calculate_snippet(self,snippet,segment):
        if snippet and snippet.data and snippet.formatter:
            text = snippet and snippet.formatter(snippet, segment)
        else:
            text = snippet and snippet.text[:]
        return text

    def get_snippet_text(self, file, snippet_name, segment, process=True):
        if file == '*':
            snippet = self.find_joker_snippet(snippet_name)
            text = self.calculate_snippet(snippet,segment)
        else:
            if file == '.':
                file = segment.filename
            snippet = file in snippets and snippet_name in snippets[file] and snippets[file][snippet_name]
            text = self.calculate_snippet(snippet,segment)
        if not text:
            msg = "snippet %s/%s is not defined" % (file, snippet_name)
            if msg not in self.warning_exclude:
                logger.warning(msg)
            return False
        logger.debug("snippet %s/%s is %s" % (file, snippet_name, text))
        if process:
            return self.processed(text, segment)
        else:
            if re.search(r"\bTEMPLATE\b", text[0]):
                logger.warning("snippet was used as parameter, will not be processed as template: %s" % text[0][0:-1])
            return text

    def processed(self, text, segment):
        line = text[0]
        if not re.search(r"\s+TEMPLATE\s+", line):
            if re.search(r"\s+WITH\s+", segment.text[0]):
                logger.warning("Using non-template snippet with parameters: %s" % segment.text[0])
            return text
        line = segment.text[0]
        try:
            if re.search(r"\s+WITH\s+", line):
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
        match = re.search(r"\s+WITH\s+(.*)$", line)
        line = match.group(1)
        while len(line) > 0:
            value_is_from_snippet = False
            match = re.search(r'(\w[\w\d_]*)\s*=\s*"(.*?)"\s*(.*)$', line)
            if not match:
                match = re.search(r"(\w[\w\d_]*)\s*=\s*'(.*?)'\s*(.*)$", line)
            if not match:
                match = re.search(r"(\w[\w\d_]*)\s*->\s*'(.*?)'\s*(.*)$", line)
                value_is_from_snippet = True
            if not match:
                match = re.search(r'(\w[\w\d_]*)\s*->\s*"(.*?)"\s*(.*)$', line)
                value_is_from_snippet = True
            if match:
                line = match.group(3)
                key = match.group(1)
                if value_is_from_snippet:
                    text = self.get_modified_text(match.group(2), segment, process=False)
                    if text:
                        text = self.chomp(text)
                        value = "".join(text[1:-1])
                    else:
                        value = "{UNDEFINED:%s}" % key
                else:
                    value = match.group(2)
                local[key] = value
            else:
                break
        return local

    def find_joker_snippet(self, snippet):
        found_nr = 0
        collected = False
        for k, v in snippets.items():
            found = snippet in v and v[snippet]
            if found:
                if collected:
                    collected.text = collected.text[:-1] + found.text[1:]
                else:
                    collected = found
                found_nr += 1
        if found_nr == 0:
            msg = "undefined snippet %s is used" % snippet
            if msg not in self.warning_exclude:
                logger.warning(msg)
        if found_nr > 1:
            msg = "used snippet %s is defined in multiple files" % snippet
            if msg not in self.warning_exclude:
                logger.warning(msg)
        return collected

    def chomp(self, text, inline=True):
        """remove the last \n if the segment is to be chomped"""
        if not re.search("TRUNCATE", text[0]):
            return text
        if len(text) < 2:
            logger.warning("segment %s is too short to truncate the last line " % text[0])
        if len(text[-2]) > 1 and text[-2][-1] == '\n' and text[-2][-2] == '\\':
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
        text = self.get_modified_text(match.group(2), segment)
        if not text:
            return
        text = self.chomp(text, False)
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
        return r'```\s*\n|END\s+SNIPPET'

    # START SNIPPET MdSnippetWriter_handle
    def handle(self, pass_nr, segment: Segment):
        startline = segment.text[0]
        match = re.search(SnippetWriter.start_line, startline)
        if not match:
            return
        text = self.get_modified_text(match.group(2), segment)
        if not text:
            return
        if len(segment.text) < 2:
            logger.warning("segment %s/%s is too short, cannot be processed" % (segment.filename, segment.name))
        else:
            text = self.chomp(text, False)
            segment.text = [segment.text[0], segment.text[1]] + \
                           text[1:-1] + \
                           [segment.text[-1]]
            segment.modified = True
    # END SNIPPET
