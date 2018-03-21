import logging
import re

from pyama.file import Segment
from pyama.segmenthandler import SegmentHandler
from pyama.template import SnippetFormatter

logger = logging.getLogger("pyama.javahandler.JavaHandler")

space = re.compile(r"\s+|=|;")


class JavaHandler(SegmentHandler):
    start_line = r'//\s*(?:FIELDS|CONSTRUCTOR|GETTERS|SETTERS|EQUALS|TOSTRING|BUILDER)'

    def __init__(self):
        self.fields = []
        self.classname = None
        self.template_parameters = None
        self.java_dict = {}

    def passes(self):
        """
        :return: this handler needs two passes
        """
        return [1, 2]

    def start(self):
        return JavaHandler.start_line

    def end(self):
        return r'//\s*END'

    def handle(self, pass_nr, segment: Segment):
        if pass_nr not in [1, 2]:
            return
        if not re.search(r".*\.java$", segment.filename):
            return
        startline = segment.text[0]
        if re.search(r'//\s*FIELDS', startline):
            if pass_nr == 1:
                self.handle_fields(segment)
            return
        if re.search(r'//\s*CONSTRUCTOR', startline):
            if pass_nr == 2:
                self.handle_constructor(segment)
            return
        if re.search(r'//\s*GETTERS', startline):
            if pass_nr == 2:
                self.handle_getters(segment)
            return
        if re.search(r'//\s*SETTERS', startline):
            if pass_nr == 2:
                self.handle_setters(segment)
            return
        if re.search(r'//\s*EQUALS', startline):
            if pass_nr == 2:
                self.handle_equals(segment)
            return
        if re.search(r'//\s*TOSTRING', startline):
            if pass_nr == 2:
                self.handle_tostring(segment)
            return
        if re.search(r'//\s*BUILDER', startline):
            if pass_nr == 2:
                self.handle_builder(segment)
            return
        if pass_nr == 1:
            self.handle_general_segment(segment)
        return

    def handle_general_segment(self, segment):
        if segment.name == "0":
            # we start a new file, forget classes we have already managed
            self.classname = None
            self.template_parameters = {}
            self.java_dict[segment.filename] = self.template_parameters

        if self.classname is None:
            for line in segment.text:
                match = re.search(r"class\s+(\w[\w\d_]*)", line)
                if match:
                    self.classname = match.group(1)
                    self.template_parameters["class"] = match.group(1)
                match = re.search(r"^\s*package\s+(.*)\s*;\s*$", line)
                if match:
                    self.template_parameters["package"] = match.group(1)
                match = re.search(r"^\s*import\s+(.*)\s*;\s*$", line)
                if match:
                    if "imports" not in self.template_parameters:
                        self.template_parameters["imports"] = []
                    self.template_parameters["imports"].append(match.group(1))

    def handle_fields(self, segment: Segment):
        self.fields = []
        for line in segment.text[1:len(segment.text) - 1]:
            # skip java comment lines
            if re.search(r"^\s*//", line):
                continue
            var = Var(line)
            self.fields.append(var)
            if "fields" not in self.template_parameters:
                self.template_parameters["fields"] = {}
            self.template_parameters["fields"][var.name] = var

    def template(self, template):
        sf = SnippetFormatter()
        return [s + "\n" for s in sf.format(template, **self.template_parameters).split("\n")][0:-1]

    def handle_constructor(self, segment):
        const_head = segment.text[1]
        match = re.search(r"\s*(private|protected|public|).*\(.*\)(.*)\{", const_head)
        if match:
            self.template_parameters["constructor_modifier"] = match.group(1)
            self.template_parameters["constructor_throws"] = match.group(2)
        else:
            logger.info("%s does not have constructor, generating a public one" % self.classname)
            self.template_parameters["constructor_modifier"] = "public"
            self.template_parameters["constructor_throws"] = ""
        for var in self.fields:
            var.need_constructor_calculate()
        text = self.template("""\
    {constructor_modifier} {class}({fields:repeat, :{{value.need_constructor:if:final {{value.type}} {{value.name}}}}}){constructor_throws}{{
{fields:repeat:{{value.need_constructor:if:        this.{{value.name}} = {{value.name}};}}
}        }}
        """)
        end_start = self.find_start(segment)
        segment.text = segment.text[0:1] + \
                       text[0:1] + \
                       segment.text[2:end_start] + \
                       text[1:] + \
                       segment.text[len(segment.text) - 1:len(segment.text)]
        segment.modified = True

    def find_start(self, segment):
        for i in range(1, len(segment.text)):
            if re.search(r"//\s*START", segment.text[i]):
                return i + 1
        return 1

    def handle_getters(self, segment):
        line = segment.text[0]
        for_all = re.search(r"for\s+all", line)
        for var in self.fields:
            var.need_getter_calculate(for_all)
            var.getter_name_calculate()

        text = self.template("""\
{fields:repeat:{{value.need_getter:if:\
    {{value.getter_modifier}}{{value.getter_modifier:if: }}{{value.type}} {{value.getter_name}}(){{{{
        return this.{{value.name}};
    }}}}
}}}""")
        segment.text = [segment.text[0]] + text + [segment.text[-1]]
        segment.modified = True

    def handle_setters(self, segment):
        line = segment.text[0]
        for_all = re.search(r"for\s+all", line)
        for var in self.fields:
            var.need_setter_calculate(for_all)
            var.setter_name_calculate()

        sf = SnippetFormatter()
        text = self.template("""\
{fields:repeat:{{value.need_setter:if:\
    {{value.setter_modifier}}{{value.setter_modifier:if: }}void {{value.setter_name}}(final {{value.type}} {{value.name}}){{{{
        this.{{value.name}} = {{value.name}};
    }}}}
}}}""")
        segment.text = [segment.text[0]] + text + [segment.text[-1]]
        segment.modified = True
        return

    def handle_equals(self, segment):
        line = segment.text[0]
        self.template_parameters["equals_with_getters"] = re.search(r"with\s+getters", line)
        self.template_parameters["equals_allow_subclass"] = re.search(r"allow\s+subclass", line)
        self.template_parameters["equals_allow_simple"] = re.search("simple", line)
        self.template_parameters["equals_allow_Objects"] = re.search("Objects", line)
        for var in self.fields:
            var.getter_name_calculate()
            var.need_equals_calculate()
            var.type_category_calculate()

        if re.search("simple", line):
            self.handle_simple_equals_and_hash_code(segment)
            return
        if re.search("Objects", line):
            self.handle_objects_equals_and_hash_code(segment)
            return
        self.handle_objects_equals_and_hash_code(segment)

    def handle_simple_equals_and_hash_code(self, segment):
        text = self.generate_simple_equals() + self.generate_simple_hash_code()
        segment.text = [segment.text[0]] + text + [segment.text[-1]]
        segment.modified = True

    def handle_objects_equals_and_hash_code(self, segment):
        text = self.generate_objects_equals() + self.generate_objects_hash_code()
        segment.text = [segment.text[0]] + text + [segment.text[-1]]
        segment.modified = True

    def generate_objects_hash_code(self):
        return self.template("""\
    @Override
    public int hashCode() {{
        return Objects.hash(\
{equals_with_getters:ifnot:{fields:repeat, :{{value.need_equals:if:{{value.name}}}}}}\
{equals_with_getters:if:{fields:repeat, :{{value.need_equals:if:{{value.getter_name}}()}}}});
    }}
""")

    def generate_simple_hash_code(self):
        self.template_parameters["need_long_tmp"] = any([var.type == "double" for var in self.fields])

        text = self.template("""\
    @Override
    public int hashCode() {{
        int result = 0;
{need_long_tmp:if:        long temp;
}{equals_with_getters:ifnot:
{fields:repeat:{{value.need_equals:if:\
        {{value.type:if=boolean:result = result * 31 + ({{value.name}} ? 1 : 0);}}\
{{value.type:if=byte:result = result * 31 + (int){{value.name}};}}\
{{value.type:if=char:result = result * 31 + (int){{value.name}};}}\
{{value.type:if=short:result = result * 31 + (int){{value.name}};}}\
{{value.type:if=int:result = result * 31 + {{value.name}};}}\
{{value.type:if=long:result = result * 31 + (int) ({{value.name}} ^ ({{value.name}} >>> 32));}}\
{{value.type:if=float:result = result * 31 + ({{value.name}} != +0.0f ? Float.floatToIntBits({{value.name}}) : 0);}}\
{{value.type:if=double:temp = Double.doubleToLongBits({{value.name}});
        result = result * 31 +  (int) (temp ^ (temp >>> 32));}}\
{{value.type_object:if:result = result * 31 + ({{value.name}} != null ? {{value.name}}.hashCode() : 0);}}\
}}
}\
}{equals_with_getters:if:
{fields:repeat:{{value.need_equals:if:\
        {{value.type:if=boolean:result = result * 31 + ({{value.getter_name}}() ? 1 : 0);}}\
{{value.type:if=byte:result = result * 31 + (int){{value.getter_name}}();}}\
{{value.type:if=char:result = result * 31 + (int){{value.getter_name}}();}}\
{{value.type:if=short:result = result * 31 + (int){{value.getter_name}}();}}\
{{value.type:if=int:result = result * 31 + {{value.getter_name}}();}}\
{{value.type:if=long:result = result * 31 + (int) ({{value.getter_name}}() ^ ({{value.getter_name}}() >>> 32));}}\
{{value.type:if=float:result = result * 31 + ({{value.getter_name}}() != +0.0f ? Float.floatToIntBits({{value.getter_name}}()) : 0);}}\
{{value.type:if=double:temp = Double.doubleToLongBits({{value.getter_name}}());
        result = result * 31 +  (int) (temp ^ (temp >>> 32));}}\
{{value.type_object:if:result = result * 31 + ({{value.getter_name}}() != null ? {{value.getter_name}}().hashCode() : 0);}}\
}}
}
}\
        return result;
    }}
""")
        return text

    def generate_objects_equals(self):
        text = self.template("""\
    @Override
    public boolean equals(Object o) {{
        if (this == o) return true;
        \
{equals_allow_subclass:if:if (!(o instanceof {class})) return false;}\
{equals_allow_subclass:ifnot:if (o == null || getClass() != o.getClass()) return false;}\


        {class} other = ({class}) o;
{equals_with_getters:ifnot:
{fields:repeat:{{value.need_equals:if:\
        {{value.type_simple:if:if ( {{value.name}} != other.{{value.name}} ) return false;}}\
{{value.type:if=float:if (Float.compare(other.{{value.name}}, {{value.name}}) != 0) return false;}}\
{{value.type:if=double:if (Double.compare(other.{{value.name}}, {{value.name}}) != 0) return false;}}\
{{value.type_object:if:if ( !Objects.equals({{value.name}},other.{{value.name}}) ) return false;}}\
}}
}}{equals_with_getters:if:
{fields:repeat:{{value.need_equals:if:\
        {{value.type_simple:if:if ( {{value.getter_name}}() != other.{{value.getter_name}}() ) return false;}}\
{{value.type:if=float:if (Float.compare(other.{{value.getter_name}}(), {{value.getter_name}}() ) != 0) return false;}}\
{{value.type:if=double:if (Double.compare(other.{{value.getter_name}}(), {{value.getter_name}}() ) != 0) return false;}}\
{{value.type_object:if:if ( !Objects.equals({{value.getter_name}}(),other.{{value.getter_name}}() ) ) return false;}}\
}}
}}        return true;
    }}
        """)
        return text

    def generate_simple_equals(self):
        sf = SnippetFormatter()
        text = self.template("""\
    @Override
    public boolean equals(Object o) {{
        if (this == o) return true;
        \
{equals_allow_subclass:if:if (!(o instanceof {class})) return false;}\
{equals_allow_subclass:ifnot:if (o == null || getClass() != o.getClass()) return false;}\


        {class} other = ({class}) o;
{equals_with_getters:ifnot:
{fields:repeat:{{value.need_equals:if:\
        {{value.type_simple:if:if ( {{value.name}} != other.{{value.name}} ) return false;}}\
{{value.type:if=float:if (Float.compare(other.{{value.name}}, {{value.name}}) != 0) return false;}}\
{{value.type:if=double:if (Double.compare(other.{{value.name}}, {{value.name}}) != 0) return false;}}\
{{value.type_object:if:if ( {{value.name}} != null ? !{{value.name}}.equals(other.{{value.name}}) : other.{{value.name}} != null ) return false;}}\
}}
}}{equals_with_getters:if:
{fields:repeat:{{value.need_equals:if:\
        {{value.type_simple:if:if ( {{value.getter_name}}() != other.{{value.getter_name}}() ) return false;}}\
{{value.type:if=float:if (Float.compare(other.{{value.getter_name}}(), {{value.getter_name}}() ) != 0) return false;}}\
{{value.type:if=double:if (Double.compare(other.{{value.getter_name}}(), {{value.getter_name}}() ) != 0) return false;}}\
{{value.type_object:if:if ( {{value.getter_name}}() != null ? !{{value.getter_name}}().equals(other.{{value.getter_name}}()) : other.{{value.getter_name}}() ) ) return false;}}\
}}
}}        return true;
    }}
        """)
        return text

    def handle_tostring(self, segment):
        line = segment.text[0]
        self.template_parameters["tostring_with_getters"] = re.search(r"with\s+getters", line)
        for var in self.fields:
            var.getter_name_calculate()
        sf = SnippetFormatter()

        text = self.template("""\
            @Override
            public String toString() {{
                final StringBuilder sb = new StringBuilder("{class}{{");
{tostring_with_getters:ifnot:{fields:repeat\
                sb.append(",")\n:\
                sb.append("{{value.name}}=").append({{value.name}});\n}}\
{tostring_with_getters:if:{fields:repeat\
                sb.append(",")\n:\
                sb.append("{{value.name}}=").append({{value.getter_name}}());\n}}\
                sb.append("}}");
                return sb.toString();
            }}
        """)
        segment.text = [segment.text[0]] + text + [segment.text[-1]]
        segment.modified = True

    def handle_builder(self, segment):
        line = segment.text[1]
        match = re.search(r"(protected|private|public).*class\s+(\w[\w\d_]*)", line)
        if not match:
            match = re.search(r"().*class\s+(\w[\w\d_]*)", line)
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
        text = self.template("""\
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
                """)
        segment.text = [segment.text[0]] + text + [segment.text[-1]]
        segment.modified = True


class Var:
    def __init__(self, line):
        self.access = "package"
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

        self.type_simple = None
        self.type_object = None

        self.setter_modifier = "public"
        self.getter_modifier = "public"
        if re.search(r".*//.*protected\s+setter", line):
            self.setter_modifier = "protected"
        if re.search(r".*//.*protected\s+getter", line):
            self.getter_modifier = "protected"
        if re.search(r".*//.*package\s+setter", line):
            self.setter_modifier = ""
        if re.search(r".*//.*package\s+getter", line):
            self.getter_modifier = ""
        if re.search(".*//.*setter", line):
            self.setter_forced = True
        if re.search(".*//.*getter", line):
            self.getter_forced = True
        if re.search(".*//.*constructor", line):
            self.constructor_forced = True
        match = re.search(r'.*//\s*builder\s+method\s+"(.*)"', line)
        if match:
            self.builder_name = match.group(1)
        else:
            self.builder_name = None
        self.builder_forced = re.search(r'.*//\s*builder', line)
        self.builder_forbidden = not not re.search(r'.*//\s*no\s*builder', line)
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

    def need_getter_calculate(self, for_all=False):
        self.need_getter = for_all or self.getter_forced or (self.access == "private" and not self.static)

    def need_setter_calculate(self, for_all=False):
        self.need_setter = for_all or self.setter_forced or (
                self.access == "private" and not self.final and not self.static)

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

    def type_category_calculate(self):
        if self.type in ["boolean", "byte", "int", "long", "char", "short"]:
            self.type_simple = True
            self.type_object = False
            return
        if self.type != "double" and self.type != "float":
            self.type_simple = False
            self.type_object = True
            return
