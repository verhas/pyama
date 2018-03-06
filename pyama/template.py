import string
import re


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
            if type(value_string) is dict:
                text = [self.format(template,key=key, value=value) for key, value in value_string.items()]
                result = match.group(1).join(text)
                return result
            return match.group(1).join([template.format(item=item) for item in value_string])
        elif spec == 'call':
            return value_string()
        elif spec.startswith('if:'):
            return (value_string and spec.partition(':')[-1]) or ''
        elif spec.startswith('ifnot:'):
            return ((not value_string) and spec.partition(':')[-1]) or ''
        else:
            return super(SnippetFormatter, self).format_field(value_string, spec)
