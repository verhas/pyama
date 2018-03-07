from pyama.segmenthandler import SegmentHandler
from pyama.file import Segment
import re
import logging
from pyama.template import SnippetFormatter

logger = logging.getLogger("pyama.javahandler.JavaHandler")

space = re.compile("\\s+|=|;")


class JavaHandler(SegmentHandler):
    start_line = '//\\s*(?:FIELDS|CONSTRUCTOR|GETTERS|SETTERS|EQUALS|TOSTRING|BUILDER)'

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
        if re.search('//\\s*BUILDER', startline):
            self.handle_builder(segment)
            return
        self.handle_general_segment(segment)
        return

    def handle_general_segment(self, segment):
        if segment.name == "0":
            # we start a new file, forget classes we have already managed
            self.classname = None
            self.template_parameters = {}
        if self.classname is None:
            for line in segment.text:
                match = re.search("class\\s+(\\w[\\w\\d_]*)", line)
                if match:
                    self.classname = match.group(1)
                    self.template_parameters["class"] = match.group(1)
                match = re.search("^\\s*package\\s+(.*)\\s*;\\s*$", line)
                if match:
                    self.template_parameters["package"] = match.group(1)
                match = re.search("^\\s*import\\s+(.*)\\s*;\\s*$", line)
                if match:
                    if "imports" not in self.template_parameters:
                        self.template_parameters["imports"] = []
                    self.template_parameters["imports"].append(match.group(1))

    def handle_fields(self, segment: Segment):
        self.fields = []
        for line in segment.text[1:len(segment.text) - 1]:
            if re.search("^\\s*//", line):
                continue
            var = Var(line)
            self.fields.append(var)
            if "fields" not in self.template_parameters:
                self.template_parameters["fields"] = {}
            self.template_parameters["fields"][var.name] = var

    def handle_constructor(self, segment):
        const_head = segment.text[1]
        match = re.search("\\s*(private|protected|public|).*\\(.*\\)(.*)\\{", const_head)
        if match:
            self.template_parameters["class_modifier"] = match.group(1)
            self.template_parameters["class_throws"] = match.group(2)
        else:
            logger.info("%s does not have constructor, generating a public one" % self.classname)
            self.template_parameters["class_modifier"] = "public"
            self.template_parameters["class_throws"] = ""
        for var in self.fields:
            var.need_constructor_calculate()
        sf = SnippetFormatter()
        text = [s + "\n" for s in sf.format("""\
    {class_modifier} {class}({fields:repeat,:{{value.need_constructor:if:final {{value.type}} {{value.name}} }} }){class_throws}{{
{fields:repeat:{{value.need_constructor:if:        this.{{value.name}} = {{value.name}};}}
}        }}
        """, **self.template_parameters).split("\n")][0:-1]
        segment.text = [segment.text[0]] + \
                       text + \
                       segment.text[len(segment.text) - 1:len(segment.text)]
        segment.modified = True

    def handle_getters(self, segment):
        line = segment.text[0]
        for_all = re.search("for\\s+all", line)
        text = []
        for var in self.fields:
            if var.need_getter_calculate() or for_all:
                text.append("    %s%s %s(){\n        return this.%s;\n    }\n" %
                            (var.getter_modifier, var.type, var.getter_name_calculate(), var.name))
        segment.text = [segment.text[0]] + text + [segment.text[-1]]
        segment.modified = True

    def handle_setters(self, segment):
        line = segment.text[0]
        for_all = re.search("for\\s+all", line)
        text = []
        for var in self.fields:
            if var.need_setter_calculate() or (for_all and var.maybe_setter_calculate()):
                text.append("    %svoid %s(final %s %s){\n        this.%s = %s;\n    }\n" %
                            (var.setter_modifier, var.setter_name_calculate(), var.type, var.name, var.name, var.name))
        segment.text = [segment.text[0]] + text + [segment.text[-1]]
        segment.modified = True

    def handle_equals(self, segment):
        line = segment.text[0]
        with_getters = re.search("with\\s+getters", line)
        allow_subclass = re.search("allow\\s+subclass", line)
        if re.search("simple", line):
            self.handle_simple_equals_and_hash_code(segment, with_getters, allow_subclass)
            return
        if re.search("Objects", line):
            self.handle_objects_equals_and_hash_code(segment, with_getters, allow_subclass)
            return
        self.handle_objects_equals_and_hash_code(segment, with_getters, allow_subclass)

    def handle_simple_equals_and_hash_code(self, segment, with_getters, allow_subclass):
        text = []
        self.generate_simple_equals(text, allow_subclass, with_getters)
        self.generate_simple_hash_code(text, with_getters)
        segment.text = [segment.text[0]] + text + [segment.text[-1]]
        segment.modified = True

    def handle_objects_equals_and_hash_code(self, segment, with_getters, allow_subclass):
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
            if not var.need_equals_calculate():
                continue
            text.append("%s%s" % (sep, var.getter_name_calculate() + "()" if with_getters else var.name))
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
            if not var.need_equals_calculate():
                continue
            variable_name = var.getter_name_calculate() + "()" if with_getters else var.name
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
            if not var.need_equals_calculate():
                continue
            variable_name = var.getter_name_calculate() + "()" if with_getters else var.name
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
            if not var.need_equals_calculate():
                continue
            variable_name = var.getter_name_calculate() + "()" if with_getters else var.name
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

    def handle_tostring(self, segment):
        line = segment.text[0]
        with_getters = re.search("with\\s+getters", line)
        text = []
        text.append("""    @Override
    public String toString() {
        final StringBuilder sb = new StringBuilder("%s{");
""" % self.classname)
        sep = ""
        for var in self.fields:
            variable_name = var.getter_name_calculate() + "()" if with_getters else var.name
            text.append('        sb.append("%s%s=").append(%s);\n' % (sep, variable_name, variable_name))
            sep = ","
        text.append("""        sb.append('}');
        return sb.toString();
    }
""")
        segment.text = [segment.text[0]] + text + [segment.text[-1]]
        segment.modified = True

    def handle_builder(self, segment):
        line = segment.text[1]
        match = re.search("(protected|private|public|).*class\\s+(\\w[\\w\\d_]*)", line)
        if match:
            self.template_parameters["builder_class_modifier"] = match.group(1)
            self.template_parameters["builder_classname"] = match.group(2)
        else:
            self.template_parameters["builder_class_modifier"] = "public"
            self.template_parameters["builder_classname"] = "Builder"

        for var in self.fields:
            var.need_builder_calculate()
            var.builder_name_calculate()

        sf = SnippetFormatter()
        text = [s + "\n" for s in sf.format("""\
    {builder_class_modifier} static class {builder_classname} {{
        private {builder_classname}(){{}}
        private {class} built = new {class}();
        public {class} build(){{
            final {class} r = built;
            built = null;
            return r;
            }}
    {fields:repeat:{{value.need_builder:if:\
        public final {builder_classname} {{value.builder_name}}(final {{value.type}} {{value.name}}){{{{
            built.{{value.name}} = {{value.name}};
            return this;
            }}}}}}
        }public static {builder_classname} builder(){{
            return new {builder_classname}();
        }}
                """, **self.template_parameters).split("\n")][0:-1]
        segment.text = [segment.text[0]] + text + [segment.text[-1]]
        segment.modified = True


class Var:
    def __init__(self, line):
        self.access = "package"
        self.type = None
        self.name = None
        self.final = False
        self.static = False
        self.type = None
        self.name = None
        self.getter_forced = False
        self.setter_forced = False
        self.constructor_forced = False

        self.assigned = not line.find("=") == -1

        self.builder_name = None
        self.getter_name = None
        self.setter_name = None
        self.need_constructor = None
        self.need_getter = None
        self.need_setter = None
        self.maybe_setter = None
        self.need_equals = None
        self.need_builder = None

        self.setter_modifier = "public "
        self.getter_modifier = "public "
        if re.search(".*//.*protected\\s+setter", line):
            self.setter_modifier = "protected "
        if re.search(".*//.*protected\\s+getter", line):
            self.getter_modifier = "protected "
        if re.search(".*//.*package\\s+setter", line):
            self.setter_modifier = ""
        if re.search(".*//.*package\\s+getter", line):
            self.getter_modifier = ""
        if re.search(".*//.*setter", line):
            self.setter_forced = True
        if re.search(".*//.*getter", line):
            self.getter_forced = True
        if re.search(".*//.*constructor", line):
            self.constructor_forced = True
        match = re.search('.*//\\s*builder\\s+method\\s+"(.*)"', line)
        if match:
            self.builder_name = match.group(1)
        else:
            self.builder_name = None
        self.builder_forced = re.search('.*//\\s*builder', line)
        self.builder_forbidden = not not re.search('.*//\\s*no\\s*builder', line)
        for tag in space.split(line):
            if tag == "final":
                self.final = True
                continue

            if tag == "static":
                self.static = True
                continue

            if tag in ["private", "protected", "public"]:
                self.access = tag
                continue

            if tag in ["transient", "volatile"]:
                continue

            if len(tag) > 0:
                if self.type is None:
                    self.type = tag
                    continue

                if self.name is None:
                    self.name = tag
                    # name is the last element we care, if there is init expression we ignore
                    break

    def builder_name_calculate(self):
        if not self.builder_name:
            self.builder_name = "with" + self.name[:1].upper() + self.name[1:]
        return self.builder_name

    def getter_name_calculate(self):
        prefix = "is" if self.type in ["boolean", "Boolean"] else "get"
        self.getter_name = prefix + self.name[:1].upper() + self.name[1:]
        return self.getter_name

    def setter_name_calculate(self):
        self.setter_name = "set" + self.name[:1].upper() + self.name[1:]
        return self.setter_name

    def need_constructor_calculate(self):
        self.need_constructor = self.constructor_forced or (self.final and not self.static and not self.assigned)
        return self.need_constructor

    def need_getter_calculate(self):
        self.need_getter = self.getter_forced or (self.access == "private" and not self.static)
        return self.need_getter

    def need_setter_calculate(self):
        self.need_setter = self.setter_forced or (self.access == "private" and not self.final and not self.static)
        return self.need_setter

    def maybe_setter_calculate(self):
        self.maybe_setter = not self.final
        return self.maybe_setter

    def need_equals_calculate(self):
        self.need_equals = not self.static
        return self.need_equals

    def need_builder_calculate(self):
        if self.builder_forbidden:
            self.need_builder = False
            return False
        self.need_builder = (self.builder_forced) or (not self.static and not self.final and not self.assigned)
        return self.need_builder
