import re

from pyama.segmenthandler import SegmentHandler


class LineNumberer(SegmentHandler):
    def __init__(self, runpass=3):
        self.runpass = runpass

    def passes(self):
        '''
        :return: snippet references are modified when all snippets are already in memory
        '''
        return [self.runpass]

    def line_numbering(self, segment):
        """ postprocess the lines in case there is any REPLACE command on the first line"""
        match = re.search(r"NUMBER\s+(.*)", segment.text[0])
        if not match:
            return segment.text
        number_spec = match.group(1)

        match = re.search(r"START\s*=(\d+)", number_spec)
        if match:
            line_number = int(match.group(1))
        else:
            line_number = 1

        match = re.search(r"STEP\s*=(\d+)", number_spec)
        if match:
            step = int(match.group(1))
        else:
            step = 1

        match = re.search(r"FORMAT\s*=\s*'([^']*)'", number_spec)
        if not match:
            match = re.search(r'FORMAT\s*=\s*"([^"]*)"', number_spec)
        if match:
            nr_format = match.group(1)
        else:
            if line_number + (len(segment.text) - 2) * step <= 10:
                nr_format = "{:d}. "
            else:
                nr_format = "{:2d}. "

        # process the intermediate lines, not the first and the last
        for i in range(1, len(segment.text) - 1):
            segment.text[i] = nr_format.format(line_number) + segment.text[i]
            line_number += step
        return segment.text

    def handle(self, pass_nr, segment):
        segment.text = self.line_numbering(segment)
        segment.modified = True
