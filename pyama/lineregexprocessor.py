import re

from pyama.segmenthandler import SegmentHandler


class LineRegexHandler(SegmentHandler):
    def __init__(self, runpass=3):
        self.runpass = runpass

    def passes(self):
        '''
        :return: snippet references are modified when all snippets are already in memory
        '''
        return [self.runpass]

    def postprocess(self, segment):
        """ postprocess the lines in case there is any REPLACE command on the first line"""
        match = re.search(r"REPLACE\s+'([^']*)'\s*->\s*'([^']*)'", segment.text[0])
        if not match:
            match = re.search(r'REPLACE\s+"([^"]*)"\s*->\s*"([^"]*)"', segment.text[0])
        if not match:
            return segment.text
        search = match.group(1)
        replace = match.group(2)
        # process the intermediate lines, not the first and the last
        for i in range(1, len(segment.text) - 1):
            segment.text[i] = re.sub(search, replace, segment.text[i])
        # save the user shooting the foot
        # may accidentally remove the new-line characters, but even then the last line has to have a new line
        if segment.text[-2][-1] != "\n":
            segment.text[-2] = segment.text[-2] + "\n"
        return segment.text

    def handle(self, pass_nr, segment):
        segment.text = self.postprocess(segment)
        segment.modified = True
