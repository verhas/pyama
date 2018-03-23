# Line skipping handler

The handler `LineSkipper` can be used to skip/delete certain lines in a segment. The typical
use is together with the snippet handlers. When a snippet is written to a segment we can
delete certain parts of the copied snippet from the segment. An example can be
seen in the `pyama.py` file in this project:

[//]: # (USE SNIPPET pyama.py/run_py SKIPPER REMOVE)
```python
from pyama.configuration import Configuration
from pyama.processor import Processor
from pyama.shellsnippet import ShellSnippet
from pyama.snippet import MdSnippetWriter, SnippetReader, SnippetMacro
from pyama.lineskipperhandler import LineSkipper

snippetWriter = MdSnippetWriter()
snippetWriter.no_warning("""
WARNING:pyama.snippet:undefined snippet whatever_my_snippet is used
WARNING:pyama.snippet:snippet */whatever_my_snippet is not defined
WARNING:pyama.snippet:snippet filename/snippetname is not defined
WARNING:pyama.snippet:snippet filename/snippetname is not defined
WARNING:pyama.snippet:snippet doc/snippet.md/xetters is not defined
WARNING:pyama.snippet:snippet pyama.py/run__py is not defined
WARNING:pyama.snippet:undefined snippet license_handler is used
WARNING:pyama.snippet:snippet */license_handler is not defined
""")
MD = Configuration().file(r".*\.md$").handler(snippetWriter, SnippetReader(),LineSkipper())
PY = Configuration().file(r".*\.py$").handler(SnippetReader(), ShellSnippet())
JAVA = Configuration().file(r".*\.java$").handler(SnippetReader(), SnippetMacro())
configs = [MD, PY, JAVA]

Processor(configs, "**/*.*").process()
``` 

## Skipping Use

In this snippet the warning switch off code may be distracting when explaining the
configuration of Pyama. What we want to display is:

[//]: # (USE SNIPPET pyama.py/run_py SKIPPER)
```python
from pyama.configuration import Configuration
from pyama.processor import Processor
from pyama.shellsnippet import ShellSnippet
from pyama.snippet import MdSnippetWriter, SnippetReader, SnippetMacro
from pyama.lineskipperhandler import LineSkipper

snippetWriter = MdSnippetWriter()
MD = Configuration().file(r".*\.md$").handler(snippetWriter, SnippetReader(),LineSkipper())
PY = Configuration().file(r".*\.py$").handler(SnippetReader(), ShellSnippet())
JAVA = Configuration().file(r".*\.java$").handler(SnippetReader(), SnippetMacro())
configs = [MD, PY, JAVA]

Processor(configs, "**/*.*").process()
``` 

The handler `LineSkipper` can be used to remove the unwanted lines.

This handler works on segments that have the keyword `SKIPPER` on the first line
of the segment and it can remove lines from the segment following special lines
in the segment. If it finds a line in the segment that says

```bash
SNIPPET SKIP 1 LINE
```

then it will remove this line and the next line from the segment. Similarly you can
also say

```bash
SNIPPET SKIP 10 LINES
```

to remove this line and the next ten lines. If there are less number of lines in the segment
following this line than the specified number then all the remaining lines will be removed.

Sometimes it is cumbersome to count the number of lines to be removed and doing so may
also not easy. In the example above inserting a new warning into the ignored
warnings string would require us to increase the number. It is also possible to
specify a regular expression that will match the last line of the lines that are
to be skipped or the line that should already not be skipped.

Using the

```bash
SNIPPET SKIP TILL "xxx"
```

will skip this line and the lines following it until it finds a line that matches
the regular expression `xxx`. Note that the line that matched the regular expression
`xxx` will not be skipped.

Using the 

```bash
SNIPPET SKIP AFTER "xxx"
```

will skip this line and the lines following it until and after it finds a line that
matches the regular expression `xxx`. Note that the line that matched the regular
expression `xxx` will also be skipped.

# Remove use

Sometimes you want to use the whole snippet without skipping lines, but you still do not
want to have the lines in the snippet that control the skipping. 
For example you want to have the code display above including the `SNIPPET SKIP ...` lines.
What we want to avoid is this:

[//]: # (USE SNIPPET pyama.py/run_py)
```python
from pyama.configuration import Configuration
from pyama.processor import Processor
from pyama.shellsnippet import ShellSnippet
from pyama.snippet import MdSnippetWriter, SnippetReader, SnippetMacro
from pyama.lineskipperhandler import LineSkipper

snippetWriter = MdSnippetWriter()
# SNIPPET SKIP AFTER '"""\)'
snippetWriter.no_warning("""
WARNING:pyama.snippet:undefined snippet whatever_my_snippet is used
WARNING:pyama.snippet:snippet */whatever_my_snippet is not defined
WARNING:pyama.snippet:snippet filename/snippetname is not defined
WARNING:pyama.snippet:snippet filename/snippetname is not defined
WARNING:pyama.snippet:snippet doc/snippet.md/xetters is not defined
WARNING:pyama.snippet:snippet pyama.py/run__py is not defined
WARNING:pyama.snippet:undefined snippet license_handler is used
WARNING:pyama.snippet:snippet */license_handler is not defined
""")
MD = Configuration().file(r".*\.md$").handler(snippetWriter, SnippetReader(),LineSkipper())
PY = Configuration().file(r".*\.py$").handler(SnippetReader(), ShellSnippet())
JAVA = Configuration().file(r".*\.java$").handler(SnippetReader(), SnippetMacro())
configs = [MD, PY, JAVA]

Processor(configs, "**/*.*").process()
``` 

To do that we should start the segment with the keywords `SKIPPER REMOVE`. This will
tell the handler to run but instead of removing the lines that are controlled by
the special lines just remove the special lines. You can see good examples
of this in this documentation markdown source file.

## Note

Note that you can have similar effect if you stop the snippet using `END SNIPPET`
where the line skipping starts and starting a new snippet with the same name after
the skipped lines. In this case the lines will be appended to the snippet. With this
approach, however, you can not have display of parts and also the full snippet.