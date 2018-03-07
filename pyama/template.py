import string
import re


def filter_empty(text):
    return filter(lambda x: not re.search("^\\s*\\Z", x, re.DOTALL), text)


class SnippetFormatter(string.Formatter):
    """World's simplest Template engine.
       Originally from  Eric Brehault
       https://makina-corpus.com/blog/metier/2016/the-worlds-simplest-python-template-engine
       """

    def __init__(self):
        super(SnippetFormatter, self).__init__()

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
