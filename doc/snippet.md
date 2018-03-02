# Snippet Handler

The snippet handler collects snippets from program source files and inserts these lines
into documentation files.

A snippet is a few lines in the source file. The first line of a snippet is a line
that contains the string `START SNIPPET` followed by an optional name. The name
should start with an alpha character and can continue with alphanumeric characters
and underscore.

The last line of the snippet is a line that contains the string `END SNIPPET`

For example the following code contains a code snippet:

```java
public static void main(String []args){
     // START SNIPPET main_java
     System.out.println("Hello, world!");
    // END SNIPPET
}
```

The code snippet contains three lines. The start and the end lines are also part of the
snippet and it is the snippet writer only that ignores them when copies the lines to the
documentation. Usually you can ignore this detail and think of this example as a one line
snippet.

Note that the string that signals the start and the end of the snippet does not need to be
at the start of the line. The line may also contain other characters, that way it is
absolutely possible to use comment characters, like `//` in case of Java, `#` in case
of python.

The handler will copy the lines of the snippet into the documents that contain
one or more lines that contain the string `USE SNIPPET`. There are two handlers in this 
module that copy the snippets into the documentation. One treats anything between the
lines containing `USE SNIPPET` and `END SNIPPET` as a copy of a snippet. The other one
looks for lines that are between `USE SNIPPET` and a line that contains three
back-tick characters. This latter can be used for markdown documentation.

The snippet to be used should be referenced after the string `USE SNIPPET`. The reference
should be the name of the file, there the snippet comes from, a `/` character and then 
the name of the snippet. For example

```bash
USE SNIPPET doc/snippet.md/main_java
here is something that would be overwritten if we ran a configuration that
     System.out.println("Hello, world!");
```

says that the file `doc/snippet.md` contains a snippet named `main_java`. If it really
is the case then the handler will replace the lines between the `USE SNIPPET` and
`END SNIPPET`. The lines that start the snippet use remain in place so that pyama can
be executed many times.

Because snippet names are usually unique and files tend to be moved between directories during
development it is a burden to specify the file most of the time.
The snippet handler allows you to use `*` in place of the file name. In that case
if there is anywhere a snippet with the given name it will be used. Note, however, that
snippet handler will not care if you have more than one snippets with the same name.
It will use the one it finds first.

When the snippet is copied the first and the last lines of the copied snippet are 
not copied. That way, for example, using the example snippet `main_java` the code
copied into the documentation will only be the  printing line:

[//]: # (USE SNIPPET */main_java)
```java
     System.out.println("Hello, world!");
```

When using the markdown handler the the copy process takes care of the code starting
three back-tick and the code ending three back-ticks. In this case the three back-ticks
on the line also used to signal the end of the lines to where the snippet is copied,
therefore there is no need to use `END SNIPPET` line.

Note, however, that the starting back-ticks SHOULD be followed by the syntax type to
help pyaman to distinguish it from the snippet ending. For examples, please
look at the raw display of the [README.md](../README.md) file.

## Markdown tips

To insert the `USE SNIPPET` string into a line into the markdown documentation
there are different ways. One is to insert HTML comment into the text:

```markdown
<!-- USE SNIPPET filename/snippetname -->
```


This use will not display the line in the documentation but it will get into the converted
HTML format. If that bothers you then you can use the empty link structure:

```markdown
[//]: # (USE SNIPPET filename/snippetname)
```

which will not even get into the HTML output of the markdown conversion.

## Configuration

To use the snippet handler you can configure it as you can see in `run.py` in 
this project. The markdown documentation of this project is maintained using
pyama.

You have to import the `Configuration` class, which you have to import to all
pyama script not matter what handlers you use. You also have to import the
`Processor`, which is also general. In addition to those you have to import
the handler classes `SnippetReader` and `MdSnippetWriter`.

In the sample script that follows we parse the `.md` and `.py` files. Pyama reads
the files that match the regular expression configured as argument to the method `file()`
and segments them using the start and end lines provided by he handlers that are
configured for that extension. When the handlers are invoked they only get
those file segments that belong to files they are configured for. 

[//]: # (USE SNIPPET run.py/run_py)
```python
from pyama.configuration import Configuration
from pyama.snippet import MdSnippetWriter, SnippetReader
from pyama.processor import Processor

MD = Configuration().file(".*\\.md$").handler(MdSnippetWriter(),SnippetReader())
PY = Configuration().file(".*\\.py$").handler(SnippetReader())
JAVA = Configuration().file(".*\\.java$").handler(SnippetReader())
configs = [MD, PY, JAVA]

Processor(configs, "**/*.*").process()
```

In the example above an `MsSnippetWriter` object and a `SnippetReader` object handles the
markdown files and another `SnippetReader` object handles the Python files. Since the snippets
are stored in a global variable in the snippet handler this work fine, though it would be
cleaner to use a single instance of `SnippetReader`.

The rest of the script is the same as in any other cases. 
