from pyama.segmenthandler import SegmentHandler
import re
import logging

logger = logging.getLogger(__name__)


class LicenseHandler(SegmentHandler):
    def __init__(self):
        self.text = []
        self.filetypes = {
            ".*\\.java$": {'line_nr': 0,
                           'matcher': "^\\s*/\\*|^\\s*\\*|^\\s*\\*/",
                           'stopper': "package|import|class",
                           'start': "/*",
                           'middle': " * ",
                           'end': " */"},
            ".*\\.py$": {'line_nr': 1,
                         'matcher': "^\\s*#",
                         'stopper': "^\\s+[^#]",  # anything that is  not a comment line
                         'start': None,
                         'middle': ' # ',
                         'end': None}
        }

    # START SNIPPET licensehandler_type
    def type(self, regex, matcher, stopper=None, line_nr=0, start=None, middle='', end=None):
        self.filetypes[regex] = {'line_nr': line_nr,
                                 'matcher': matcher,
                                 'stopper': stopper,
                                 'start': start,
                                 'middle': middle,
                                 'end': end}
        # END SNIPPET

    def license(self, filename):
        logger.info("reading license text from %s" % filename)
        with open(filename, 'r') as f:
            for line in f:
                self.text.append(line)
        logger.debug("license text is \n%s\n" % "".join(self.text))

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
        if not prefixes:
            logger.info("File %s is not processed" % segment.filename)
            return

        if len(self.text) == 0:
            self.license("LICENSE.txt")

        logger.info("file %s is processed from %d with %s %s %s" %
                    (segment.filename, prefixes['line_nr'], prefixes['start'], prefixes['middle'], prefixes['end']))

        first_license_line = prefixes['line_nr']
        while first_license_line < len(segment.text) and \
                not re.search(prefixes['matcher'], segment.text[first_license_line]) and \
                not re.search(prefixes['stopper'], segment.text[first_license_line]):
            first_license_line += 1
        license_found = first_license_line != len(segment.text) and \
                        not re.search(prefixes['stopper'], segment.text[first_license_line])
        if license_found:
            logging.info("old license was found starting on line %d" % first_license_line)
            last_license_line = first_license_line
            while last_license_line < len(segment.text) and re.search(prefixes['matcher'], segment.text[last_license_line]):
                last_license_line += 1
            if last_license_line == len(segment.text):
                last_license_line -= 1

        text = [prefixes['start'] + "\n"] if prefixes['start'] is not None else []
        for line in self.text:
            text.append(prefixes['middle'] + line)
        if prefixes['end'] is not None:
            text.append(prefixes['end'] + "\n")
        if license_found:
            logger.info("replacing license text")
            segment.text = segment.text[:first_license_line] + text + segment.text[last_license_line:]
        else:
            logger.info("inserting license text")
            segment.text = segment.text[:prefixes['line_nr']] + text + segment.text[prefixes['line_nr']:]
        segment.modified = True
