# PySnippet runs python code

The `PySnippet` can execute python code written right into the snippet code. This
can be handy when some of the snippet text is computable and the templating
does not provide enough functionality but writing a special segment handler for the
purpose is an overkill. In that case you can configure `PySnippet` to run python code
and the output of the code executed will become the text of the snippet that can be
referenced and used.

The handler runs in the first pass unless it is configured differently using the
`runpass` argument of the constructor.

To use the handler you can configure in your main script:

```python
from pyama.pysnippet import PySnippet

CONF = Configuration().file(r".*\.extension$").handler(PySnippet(runpass=[1]))
Processor([CONF], "**/*.*").process()
```

A Python snippet starts with a line that contains `PYTHON SNIPPET` and
ends with `END SNIPPET`. For example the

```python
PYTHON SNIPPET numbers GLOBALS="*"
for i in range(0,3):
  print(i)
END SNIPPET
```

will create the snippet named `numbers` that will contain three lines containing the
numbers 0, 1 and 2. The numbers are "printed" by the script and thus it becomes the
content of the snippet. If the script throws exception or prints anything to the
error output Pyama will print an ERROR into the output log.

The parameter `GLOBALS` can be used to define the globals that the script will use.
You can name distinct sets of globals. If there is no `GLOBALS` defined then the
set named `_` (single underscore character) will be used. That way no using
`GLOBALS` is the same as `GLOBALS="_"`. Using globals you can separate the
different scripts so that their global variables, methods, whatevers will not mix up.

The specially named globals `*` (star character) is the default globals. If you
specify `GLOBALS="*"` for a snippet you can access the globals of pyama from the
script. Use it with great care.

The scripts can communicate with each other through globals and they are executed
withing a file in the other they appear. However, there is no guarantee for any ordering
of script execution, which are in different files.