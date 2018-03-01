from pyama.file import Segment, File
import re
import logging

logger = logging.getLogger(__name__)


class Factory:
    def reader(self, configurations, filename):
        for configuration in configurations:
            for regex in configuration.filename_regexes:
                if re.search(regex, filename):
                    return FileReader(filename, regexes=configuration.regexes)


class FileReader:
    def __init__(self, filename, regexes=[]):
        '''
        Create a new file reader that will read the file when `read` is invoked.

        :param filename: the name of the file to read
        :param regexes: Tuples of start and end regular expressions.
        The regular expressions that are used to identify the start of a new segment are the first in the tuple, and
        the regular expression to identify the end of a segment are the second in the tuple.
        If any of the start regular expressions matches then a new segment is created, added to the list of the
        segments and the name is identified by group(1) matching the start regex. The line that matches is added to the
        segment as first line.
        '''
        self.filename = filename.replace('\\','/')
        self.regexes = regexes
        self.segment_number = 0

    def _startsegment(self, line):
        """
        Check the line against the regular expressions.
        :param line: the line to check against the regular expressions
        :param regexes: the iterable of the regular expressions
        :return: A tulpe (match, name, regex) where
        match is False when there is no start regex mathing the line and then the returned value is (False, None,None)
        When there is a match then the returned tuple is (True,name,regex), where
        name is the name of the segment, aither from the first capture group or the next generated number
        regex is the segment end matching regular expression
        """
        for regex in self.regexes:
            match = re.search(regex[0], line)
            if match:
                if match.lastindex and len(match.group(1)) > 0:
                    logger.debug("line '%s' matches '%s' and name is '%s'" % (line, regex, match.group(1)))
                    return True, match.group(1), regex[1]
                else:
                    name = self.next_segment()
                    logger.debug("line '%s' matches '%s' and name is '%s'" % (line, regex, name))
                    return True, name, regex[1]
        return False, None, None

    def next_segment(self):
        """
        Create an artifical numbered segment if the segment is not named
        :return: the next number for the new segment in the file.
        """
        name = "%d" % self.segment_number
        self.segment_number += 1
        return name

    def read(self):
        """
        Read the file and split up into segments
        :return: the File object that contains the segments of the file
        """
        segments = []
        segment = None
        end_regex = None
        with open(self.filename, 'r') as f:
            for line in f:
                is_start, name, end_regex_ = self._startsegment(line)
                if is_start:
                    old = segment
                    segment = Segment(name, self.filename)
                    if old is not None:
                        old.next = segment
                    segment.previous = old
                    segments.append(segment)
                    end_regex = end_regex_
                    segment.add(line)
                    continue

                if end_regex and re.search(end_regex, line):
                    logger.debug("line '%s' matches '%s' segment ending" % (line, end_regex))
                    segment.add(line)
                    segment = None
                    end_regex = None
                    continue

                if segment is None:
                    name = self.next_segment()
                    logger.debug("Creating new unnamed segment '%s'" % name)
                    segment = Segment(name, self.filename)
                    segments.append(segment)

                segment.add(line)

        return File(self.filename, segments)
