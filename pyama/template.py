import re
import string


def filter_empty(text):
    return filter(lambda x: not re.search(r"^\s*\Z", x, re.DOTALL), text)


class SnippetFormatter(string.Formatter):
    """World's simplest Template engine.
       Originally from  Eric Brehault
       https://makina-corpus.com/blog/metier/2016/the-worlds-simplest-python-template-engine
       """

    def __init__(self):
        self.local = {}
        super(SnippetFormatter, self).__init__()

    def get_value(self, key, args, kwargs):
        if isinstance(key, int):
            return args[key]
        else:
            if key in self.local:
                return self.local[key]
            if key in kwargs:
                return kwargs[key]
            return "{UNDEFINED:%s}" % key

    def format_field(self, value_string, spec):
        match = re.search("repeat([^:]*):(.*)", spec, re.DOTALL) or \
                re.search("repeat'(.*?)':(.*)", spec, re.DOTALL) or \
                re.search('repeat"(.*?)":(.*)', spec, re.DOTALL)
        if match:
            template = match.group(2)
            sep = match.group(1)
            if type(value_string) is dict:
                text = filter_empty(
                    [self.format(template, key=key, value=value) for key, value in value_string.items()])
                result = sep.join(text)
                return result
            text = filter_empty([template.format(item=item) for item in value_string])
            result = sep.join(text)
            return result
        if spec == 'call':
            return value_string()
        if spec.startswith('if:'):
            return (value_string and spec.partition(':')[-1]) or ''
        match = re.search("if=(.*?):", spec)
        if match:
            return (value_string == match.group(1) and spec.partition(':')[-1]) or ''
        if spec.startswith('ifnot:'):
            return ((not value_string) and spec.partition(':')[-1]) or ''
        match = re.search("ifnot=(.*?):", spec)
        if match:
            return (value_string != match.group(1) and spec.partition(':')[-1]) or ''

        return super(SnippetFormatter, self).format_field(value_string, spec)

    # original formatter was not designed to work with complex templates and thus it stops after 3 level of
    # nesting in templates
    def _vformat(self, format_string, args, kwargs, used_args, recursion_depth, auto_arg_index=0):
        # any recursion_depth > -1 is okay, recursive call goes through this method, and is reset
        return super(SnippetFormatter, self)._vformat(format_string, args, kwargs, used_args, 0, auto_arg_index=0)
