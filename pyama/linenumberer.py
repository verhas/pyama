import re

from pyama.segmenthandler import SegmentHandler


class LineNumberer(SegmentHandler):
    def __init__(self, runpass=[3]):
        self.runpass = runpass

    def passes(self):
        '''
        :return: snippet references are modified when all snippets are already in memory
        '''
        return self.runpass

    def line_numbering(self, segment):
        """ postprocess the lines in case there is any REPLACE command on the first line"""
        match = re.search(r"NUMBER\b(.*)", segment.text[0])
        if not match:
            return segment.text
        number_spec = match.group(1)

        match = re.search(r"START=(\d+)", number_spec)
        if match:
            line_number = int(match.group(1))
        else:
            line_number = 1

        match = re.search(r"STEP=(\d+)", number_spec)
        if match:
            step = int(match.group(1))
        else:
            step = 1

        match = re.search(r"LINES=(-?\d*):(-?\d*)", number_spec)
        if match:
            if match.group(1):
                start = int(match.group(1))
            else:
                start = 1
            if match.group(2):
                end = int(match.group(2))
            else:
                end = -1
            lines = (start, end)
        else:
            lines = (1, -1)
        # calculate the absolute and non-negative positive indices
        if lines[0] < 0:
            lines = (lines[0] + len(segment.text), lines[1])
        if lines[1] < 0:
            lines = (lines[0], lines[1] + len(segment.text))

        # ensure limits are in the line indexing range
        lines = (max(0, lines[0]), max(0, lines[1]))
        lines = (min(lines[0], len(segment.text)), min(lines[1], len(segment.text)))

        match = re.search(r"FORMAT='([^']*)'", number_spec)
        if not match:
            match = re.search(r'FORMAT="([^"]*)"', number_spec)
        if match:
            nr_format = match.group(1)
        else:
            width_diff = str(len(str(line_number + (lines[1] - 1 - lines[0]) * step)))
            nr_format = "{:" + width_diff + "d}. "

        # process the intermediate lines, not the first and the last
        i = lines[0]
        while i < lines[1]:
            segment.text[i] = nr_format.format(line_number) + segment.text[i]
            line_number += step
            i += 1
        return segment.text

    def handle(self, pass_nr, segment):
        segment.text = self.line_numbering(segment)
        segment.modified = True
