from pyama.segmenthandler import SegmentHandler
from pyama.file import Segment
import re
import logging

LOGGER = logging.getLogger("pyama.javahandler.JavaHandler")

space = re.compile("\\s+|=|;")


class JavaHandler(SegmentHandler):
    start_line = '//\\s*(?:FIELDS|CONSTRUCTOR|GETTERS|SETTERS|EQUALS|TOSTRING)'

    def __init__(self):
        self.fields = []
        self.classname = None

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
            self.handle_fields(segment)
            return
        if re.search('//\\s*CONSTRUCTOR', startline):
            self.handle_constructor(segment)
            return
        if re.search('//\\s*GETTERS', startline):
            self.handle_getters(segment)
            return
        if re.search('//\\s*SETTERS', startline):
            self.handle_setters(segment)
            return
        if re.search('//\\s*EQUALS', startline):
            self.handle_equals(segment)
            return
        if re.search('//\\s*TOSTRING', startline):
            self.handle_tostring(segment)
            return
        self.handle_general_segment(segment)
        return

    def handle_general_segment(self, segment):
        if segment.name == "0":
            self.classname = None
        if self.classname is not None:
            for line in segment.text:
                match = re.search("class\\s+(\\w[\\w\\d_]*)", line)
                if match:
                    self.classname = match.group(1)

    def handle_fields(self, segment: Segment):
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

    def handle_constructor(self, segment):
        const_head = segment.text[1]
        match = re.search("(.*)\\(.*\\)(.*)", const_head)
        if match:
            const_head = match.group(1) + "("
            sep = ""
            for var in self.fields:
                if var.need_constructor():
                    const_head += sep + "final " + var.type + " " + var.name
                    sep = ", "
            const_head += ")" + match.group(2) + "\n"

        else:
            LOGGER.error("The line '%s' can not be processed as constructor head")
        text = []
        for var in self.fields:
            if var.need_constructor():
                text.append("        this.%s = %s;\n" % (var.name, var.name))

        segment.text = [segment.text[0], const_head] + \
                       text + \
                       segment.text[len(segment.text) - 2:len(segment.text)]
        segment.modified = True

    def handle_getters(self, segment):
        line = segment.text[0]
        for_all = re.search("for\\s+all", line)
        text = []
        for var in self.fields:
            if var.need_getter() or for_all:
                text.append("    public %s %s(){\n        return this.%s;\n    }\n" % (
                    var.type, var.getter_name(), var.name))
        segment.text = [segment.text[0]] + text + [segment.text[-1]]
        segment.modified = True

    def handle_setters(self, segment):
        line = segment.text[0]
        for_all = re.search("for\\s+all", line)
        text = []
        for var in self.fields:
            if var.need_setter() or (for_all and var.maybe_setter()):
                text.append("    public void %s(final %s %s){\n        this.%s = %s;\n    }\n" % (
                    var.setter_name(),
                    var.type, var.name, var.name, var.name))
        segment.text = [segment.text[0]] + text + [segment.text[-1]]
        segment.modified = True

    def handle_equals(self, segment):
        line = segment.text[0]
        with_getters = re.search("with\\s+getters", line)
        if re.search("simple", line):
            self.handle_simple_equals_and_hash_code(segment, with_getters)
            return
        if re.search("Objects", line):
            self.handle_objects_equals_and_hash_code(segment, with_getters)
            return
        self.handle_simple_equals_and_hash_code(segment, with_getters)

    def handle_simple_equals_and_hash_code(self, segment, with_getters):
        line = segment.text[0]
        allow_subclass = re.search("allow\\s+subclass", line)
        text = []
        self.generate_simple_equals(text, allow_subclass, with_getters)
        self.generate_simple_hash_code(text, with_getters)
        segment.text = [segment.text[0]] + text + [segment.text[-1]]
        segment.modified = True

    def handle_objects_equals_and_hash_code(self, segment, with_getters):
        line = segment.text[0]
        allow_subclass = re.search("allow\\s+subclass", line)
        text = []
        self.generate_objects_equals(text, allow_subclass, with_getters)
        self.generate_objects_hash_code(text, with_getters)
        segment.text = [segment.text[0]] + text + [segment.text[-1]]
        segment.modified = True

    def generate_objects_hash_code(self, text, with_getters):
        text.append("""    @Override
    public int hashCode() {
        return Objects.hash(""")
        sep = ""
        for var in self.fields:
            if not var.need_equals():
                continue
            text.append("%s%s" % (sep, var.getter_name() + "()" if with_getters else var.name))
            sep = ", "
        text.append(");\n    }\n")

    def generate_simple_hash_code(self, text, with_getters):
        text.append("""    @Override
    public int hashCode() {
        int result = 0;""")
        if any([var.type == "double" for var in self.fields]):
            text.append("\n        long temp;\n")
        line_start = "\n        result = result * 31 + "

        for var in self.fields:
            if not var.need_equals():
                continue
            variable_name = var.getter_name() + "()" if with_getters else var.name
            if var.type == "boolean":
                text.append(line_start + "(%s ? 1 : 0);" % variable_name)
                continue
            if var.type in ["byte", "char"]:
                text.append(line_start + "(int)%s;" % variable_name)
                continue
            if var.type == "int":
                text.append(line_start + "%s;" % variable_name)
                continue
            if var.type == "long":
                text.append(line_start + "(int) (%s ^ (%s >>> 32));" % (variable_name, variable_name))
                continue
            if var.type == "float":
                text.append(
                    line_start + "(%s != +0.0f ? Float.floatToIntBits(%s) : 0);" % (variable_name, variable_name))
                continue
            if var.type == "double":
                text.append("\n        temp = Double.doubleToLongBits(%s);" % variable_name)
                text.append(line_start + " (int) (temp ^ (temp >>> 32));")
                continue
            text.append(line_start + "(%s != null ? %s.hashCode() : 0);" % (variable_name, variable_name))
            continue
        text.append("\n        return result;\n    }\n")

    def generate_objects_equals(self, text, allow_subclass, with_getters):
        classtest = self.create_classtest(allow_subclass)
        self.equals_start(classtest, text)
        for var in self.fields:
            if not var.need_equals():
                continue
            variable_name = var.getter_name() + "()" if with_getters else var.name
            if var.type in ["boolean", "byte", "int", "long", "char", "short"]:
                text.append("        if ( %s != other.%s ) return false;\n" % (variable_name, variable_name))
                continue
            if var.type == "float":
                text.append(
                    "        if (Float.compare(other.%s, %s) != 0) return false;\n" % (variable_name, variable_name))
                continue
            if var.type == "double":
                text.append(
                    "        if (Double.compare(other.%s, %s) != 0) return false;\n" % (variable_name, variable_name))
                continue
            text.append("        if ( !Objects.equals(%s,other.%s) ) return false;\n" % (variable_name, variable_name))
        text.append("        return true;\n    }\n")
        return text

    def generate_simple_equals(self, text, allow_subclass, with_getters):
        classtest = self.create_classtest(allow_subclass)
        self.equals_start(classtest, text)
        for var in self.fields:
            if not var.need_equals():
                continue
            variable_name = var.getter_name() + "()" if with_getters else var.name
            if var.type in ["boolean", "byte", "int", "long", "char", "short"]:
                text.append("        if ( %s != other.%s ) return false;\n" % (variable_name, variable_name))
                continue
            if var.type == "float":
                text.append(
                    "        if (Float.compare(other.%s, %s) != 0) return false;\n" % (variable_name, variable_name))
                continue
            if var.type == "double":
                text.append(
                    "        if (Double.compare(other.%s, %s) != 0) return false;\n" % (variable_name, variable_name))
                continue
            text.append("        if (%s != null ? !%s.equals(other.%s) : other.%s != null) return false;\n" % (
                variable_name, variable_name, variable_name, variable_name))
        text.append("        return true;\n    }\n")
        return text

    def equals_start(self, classtest, text):
        text.append("""    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        """ + classtest + """        

        %s other = (%s) o;

""" % (self.classname, self.classname))

    def create_classtest(self, allow_subclass):
        classtest = "if (!(o instanceof %s)) return false;" % self.classname \
            if allow_subclass \
            else "if (o == null || getClass() != o.getClass()) return false;"
        return classtest

    def handle_tostring(self,segment):
        line = segment.text[0]
        with_getters = re.search("with\\s+getters", line)
        text = []
        text.append("""    @Override
    public String toString() {
        final StringBuilder sb = new StringBuilder("%s{");
""" % self.classname)
        for var in self.fields:
            variable_name = var.getter_name() + "()" if with_getters else var.name
            text.append('        sb.append("%s=").append(%s);\n' % (variable_name,variable_name))
        text.append("""        sb.append('}');
        return sb.toString();
    }
""")
        segment.text = [segment.text[0]] + text + [segment.text[-1]]
        segment.modified = True

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

    def getter_name(self):
        prefix = "is" if self.type in ["boolean", "Boolean"] else "get"
        return prefix + self.name[:1].upper() + self.name[1:]

    def setter_name(self):
        return "set" + self.name[:1].upper() + self.name[1:]

    def need_constructor(self):
        return self.final and not self.static and not self.assigned

    def need_getter(self):
        return self.access == "private" and not self.static

    def need_setter(self):
        return self.access == "private" and not self.final and not self.static

    def maybe_setter(self):
        return not self.final

    def need_equals(self):
        return not self.static
