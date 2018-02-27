from pyama.segmenthandler import SegmentHandler
import re


class LicenseHandler(SegmentHandler):
    def __init__(self):
        self.text = []
        self.filetypes = {".*\\.java$": [0, "^\\s*/\\*|^\\s*\\*|^\\s*\\*/", "/*", " * ", " */"],
                          ".*\\.py$": [1, "^\\s*#", None, ' # ', None]
                          }

    def license(self, filename):
        with open(filename, 'r') as f:
            for line in f:
                self.text.append(line)

    def passes(self):
        return [1]

    def start(self):
        return None

    def end(self):
        return None

    def handle(self, pass_nr, segment):
        if segment.name != "0":
            return
        prefixes = None
        for type in self.filetypes.keys():
            if re.search(type, segment.filename):
                prefixes = self.filetypes[type]
                break
        prefixes = [0, None, '.+', None] if prefixes is None else prefixes

        first_license_line = prefixes[0]
        while first_license_line < len(segment.text) and not re.search(prefixes[1], segment.text[first_license_line]):
            first_license_line += 1
        license_found =  first_license_line != len(segment.text)
        if license_found:
            last_license_line = first_license_line
            while last_license_line < len(segment.text) and re.search(prefixes[1], segment.text[last_license_line]):
                last_license_line += 1
            if last_license_line == len(segment.text):
                last_license_line -= 1

        text = [prefixes[2] + "\n"] if prefixes[2] is not None else []
        for line in self.text:
            text.append(prefixes[3] + line)
        if prefixes[4] is not None:
            text.append(prefixes[4] + "\n")
        if license_found:
            segment.text = segment.text[:first_license_line] + text + segment.text[last_license_line+1:]
        else:
            segment.text = text + segment.text
        segment.modified = True
