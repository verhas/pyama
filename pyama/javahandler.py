from pyama.segmenthandler import SegmentHandler
from pyama.file import Segment
import re
import logging

LOGGER = logging.getLogger("pyama.javahandler.JavaHandler")

space = re.compile("\\s+|=|;")


def _need_constructor(var):
    return var.final and not var.static and not var.assigned


class JavaHandler(SegmentHandler):
    start_line = '//\\s*(?:FIELDS|CONSTRUCTOR|GETTERS|SETTERS|EQUALS)'

    def __init__(self):
        self.fields = []

    def passes(self):
        """
        :return: this handler does it all in one pass
        """
        return [1]

    def start(self):
        return JavaHandler.start_line

    def end(self):
        return '//\\s*END'

    def handle(self, pass_nr, segment: Segment):
        if not re.search(".*\\.java$", segment.filename):
            return
        startline = segment.text[0]
        if re.search('//\\s*FIELDS', startline):
            self.handle_fields(pass_nr, segment)
            return
        if re.search('//\\s*CONSTRUCTOR', startline):
            self.handle_constructor(pass_nr, segment)
            return
        if re.search('//\\s*GETTERS', startline):
            self.handle_getters(pass_nr, segment)
            return
        if re.search('//\\s*SETTERS', startline):
            self.handle_setters(pass_nr, segment)
            return
        if re.search('//\\s*EQUALS', startline):
            self.handle_equals(pass_nr, segment)
            return
        return

    def handle_fields(self, pass_nr, segment: Segment):
        self.fields = []
        for line in segment.text[1:len(segment.text) - 1]:
            if re.search("\\s*//", line):
                continue
            var = Var()
            var.assigned = not line.find("=") == -1
            for tag in space.split(line):
                if tag == "final":
                    var.final = True
                    continue

                if tag == "static":
                    var.static = True
                    continue

                if tag in ["private", "protected", "public"]:
                    var.access = tag
                    continue

                if tag in ["transient", "volatile"]:
                    continue

                if len(tag) > 0:
                    if var.type is None:
                        var.type = tag
                        continue

                    if var.name is None:
                        var.name = tag
                        break

            self.fields.append(var)

    def handle_constructor(self, pass_nr, segment):
        const_head = segment.text[1]
        match = re.search("(.*)\\(.*\\)(.*)", const_head)
        if match:
            const_head = match.group(1) + "("
            sep = ""
            for var in self.fields:
                if _need_constructor(var):
                    const_head += sep + "final " + var.type + " " + var.name
                    sep = ", "
            const_head += ")" + match.group(2) + "\n"

        else:
            LOGGER.error("The line '%s' can not be processed as constructor head")
        text = []
        for var in self.fields:
            if _need_constructor(var):
                text.append("        this.%s = %s;\n" % (var.name, var.name))

        segment.text = [segment.text[0], const_head] + \
                       text + \
                       segment.text[len(segment.text) - 2:len(segment.text) ]
        segment.modified = True

    def handle_getters(self, pass_nr, segment):
        pass

    def handle_setters(self, pass_nr, segment):
        pass

    def handle_equals(self, pass_nr, segment):
        pass


class Var:
    def __init__(self):
        self.access = "package"
        self.type = None
        self.name = None
        self.final = False
        self.static = False
        self.type = None
        self.name = None
        self.assigned = None
