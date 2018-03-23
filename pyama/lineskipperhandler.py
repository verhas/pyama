import re

from pyama.segmenthandler import SegmentHandler


class LineSkipper(SegmentHandler):
    def __init__(self, runpass=[3]):
        self.runpass = runpass

    def passes(self):
        '''
        :return: snippet references are modified when all snippets are already in memory
        '''
        return self.runpass

    def remove(self, segment, i):
        segment.text = segment.text[:i] + segment.text[i + 1:]
        segment.modified = True

    def remove_skip(self, segment):
        i = 1
        while i < len(segment.text) - 1:
            if re.search(r"SNIPPET\s+SKIP", segment.text[i]):
                self.remove(segment,i)
                continue
            i += 1

    def skip_lines(self, segment):
        i = 1
        skipping = False
        skip_stop = None
        skip_lines = 0
        including = False
        while i < len(segment.text) - 1:
            if skipping:
                if skip_lines > 0:
                    skip_lines -= 1
                    self.remove(segment,i)
                    if skip_lines == 0:
                        skipping = False
                    continue
                if re.search(skip_stop, segment.text[i]):
                    skipping = False
                    skip_stop = None
                    if including: self.remove(segment,i)
                    continue
                else:
                    self.remove(segment,i)
                    continue
            else:
                match = re.search(r"SNIPPET\s+SKIP\s+(TILL|AFTER)\s+('|\")(.*?)\2", segment.text[i])
                if match:
                    including = match.group(1) == "AFTER"
                    skip_stop = match.group(3)
                    self.remove(segment,i)
                    skipping = True
                    continue

                match = re.search(r"SNIPPET\s+SKIP\s+(\d+)\s+LINES?", segment.text[i])
                if match:
                    skip_lines = int(match.group(1))
                    self.remove(segment,i)
                    skipping = True
                    continue

                i += 1

        return segment.text

    def handle(self, pass_nr, segment):
        startline = segment.text[0]
        if not re.search(r"SKIPPER", startline):
            return
        if re.search(r"SKIPPER\s+REMOVE", startline):
            self.remove_skip(segment)
        else:
            self.skip_lines(segment)
