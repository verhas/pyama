import logging
import re

from pyama.segmenthandler import SegmentHandler

logger = logging.getLogger(__name__)


class RegexHandler(SegmentHandler):
    def __init__(self, runpass=[3]):
        self.runpass = runpass

    def passes(self):
        '''
        :return: snippet references are modified when all snippets are already in memory
        '''
        return self.runpass

    def get_replace_tuples(self, line):
        tuples = []
        while True:
            match = re.search(r'(\'|")(.*?)\1\s*->\s*(\'|")(.*?)\3(.*)$', line)
            if not match: break
            tuple = (match.group(2), match.group(4))
            line = match.group(5)
            tuples.append(tuple)
        return tuples

    def get_kill_regexes(self, line):
        regexes = []
        while True:
            match = re.search(r'(\'|")(.*?)\1\s*(.*)$', line)
            if not match: break
            line = match.group(3)
            regexes.append(match.group(2))
        return regexes

    def postprocess(self, segment):
        """ postprocess the lines in case there is any REPLACE command on the first line"""
        match = re.search(r"REPLACE\s+(.*)$", segment.text[0])
        if match:
            replaces = self.get_replace_tuples(match.group(1))
        else:
            replaces = None
        match = re.search(r"KILL (.*)",segment.text[0])
        if match:
            kills = self.get_kill_regexes(match.group(1))
        else:
            kills = None

        if replaces is None and kills is None:
            return segment.text

        # process the intermediate lines, not the first and the last
        i = 1
        while i < len(segment.text) - 1:
            killed = False
            if kills is not None:
                for kill in kills:
                    if re.search(kill,segment.text[i]):
                        segment.text = segment.text[:i]+segment.text[i+1:]
                        killed = True
                        break

            if killed:
                continue

            if replaces is not None:
                for replace in replaces:
                    segment.text[i] = re.sub(replace[0], replace[1], segment.text[i])
            i += 1

        # save the user from shooting the foot
        # may accidentally remove the new-line characters, but even then the last line has to have a new line
        if segment.text[-2][-1] != "\n":
            segment.text[-2] = segment.text[-2] + "\n"
        return segment.text

    def handle(self, pass_nr, segment):
        segment.text = self.postprocess(segment)
        segment.modified = True
