import string


class SnippetFormatter(string.Formatter):
    """World's simplest Template engine.
       Originally from  Eric Brehault
       https://makina-corpus.com/blog/metier/2016/the-worlds-simplest-python-template-engine
       """

    def format_field(self, value, spec):
        if spec.startswith('repeat:'):
            template = spec.partition(':')[-1]
            if type(value) is dict:
                value = value.items()
            return ''.join([template.format(item=item) for item in value])
        elif spec == 'call':
            return value()
        elif spec.startswith('if:'):
            return (value and spec.partition(':')[-1]) or ''
        elif spec.startswith('ifnot:'):
            return ((not value) and spec.partition(':')[-1]) or ''
        else:
            return super(SnippetFormatter, self).format_field(value, spec)
