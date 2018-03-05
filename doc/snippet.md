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
if there is anywhere a snippet with the given name it will be used. If there are more than one
snippets with that name then the snippet handler will concatenate them.

Another shorthand is to use a `.` (dot) as file name. In that case we refer to the named
snippet defined in the same file.

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
therefore there is no need to use `END SNIPPET` line. In some cases you may want to insert
a snippet that does not go into a verbatim code segment. In these cases you can use the
`END SNIPPET` string probbaly in the form of 

```markdown
[//]: # (END SNIPPET)
```

Note, however, that the starting back-ticks SHOULD be followed by the syntax type to
help pyaman to distinguish it from the snippet ending. For examples, please
look at the raw display of the [README.md](../README.md) file.

## TRUNCATE new line from segment

In some cases you want a snippet, when used be part of a line. But segments start with
a segment start line and they also end with a segment ending line and thus the last line
is always terminated with a new line.

If you use the keyword `TRUNCATE` in the starting line of the snippet and the last
characters of the last line before the snippet terminating line are `\\n` (backslash
and new line) then they will be removed when the snippet is used.   

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

## Macro resolution

There is a class `SnippetMacro` in the `snippet` package that can help to use template files
that contain macros. Macros are placeholders in snippets between `{` and `}` characters.
The simplest macros are just identifiers. `SnippetMacro` maintains a dictionary that
assigns value to the identifiers and when a template snippet is used these macros
are replaced by the assigned value.

### Template format

The templating supports more complex macros. If the identifier is followed by a
colon and a special keyword then the assigned value is evaluated in a different way. The
keywords supported are

* `repeat` will repeat the text following the colon followed by the keyword for each element
of the assigned value in case it is iterable or a dictionary. It is not possible to have
such values using the snippet macros. This possibility is there for extra segment
handlers that may want to put such value into the dictionary.

* `call` will invoke the value if it is callable. It is not possible to have
such values using the snippet macros. This possibility is there for extra segment
handlers that may want to put such value into the dictionary.

* `if` will include tthe text following the colon followed by the keyword if the value 
evaluates `True`

* `ifnot` will include tthe text following the colon followed by the keyword if the value 
evaluates `False`. (For example empty string.)

The templating engine is implemented in the file `pyama/template.py`. It is 24 lines and
it is documented in detail on the web page
[The world's simplest Python template engine](https://makina-corpus.com/blog/metier/2016/the-worlds-simplest-python-template-engine).

### Template snippet

To signal that a snippet should be used as a template and the macros should be resolved
the SNIPPET START line should contain the word `TEMPLATE`, reasonably following the name 
of the snippet.

When the macro resolution runs it is an error if some of the macros are not defined. In this case
the text of the snippet is copied verbatim to the segment where it is used and pyama will log
a warning, also giving information about the first key that it did not find.

### Defining values

There are two ways to define parameters for the templates. One is to configure `SnippetMacro`
to run as segment handler and collect key/value pairs from the files it processes. `SnippetMacro`
itself does not define any segment start and end pattern, but it processes all lines of the
segments and collects the key/values. If it finds a line that looks `MATCH regex` then it
starts to use the `regex` to match the following lines.

The regular expression should have exactly two capturing groups. The first one will be used
as the key and the second as the value when a line matches.

The matching process ends at the end of each file or when a line containing the string`NO MATCH`
is found. In a java file you can have something like

```java
// MATCH \s+(\w+)\s*=\s*(\d+) 
public static final int VERSION=5
// NO MATCH
```

This will put the value `5` into the global macro dictionary with the key `VERSION`.
A template snippet may reference the version in the following passes as `{VERSION}`. 

The other is to use the keyword `WITH`
following the `USE SNIPPET` and the snippet reference. The `WITH` keyword has to be followed
by space separated key/value definitions. For example

```markdown
USE SNIPPET ./xetters WITH xetters="setters" xetter="setter" XETTERS="SETTERS" and_not_final=" and not `final`"
``` 

The format of the key/value definition is `key="string value"`, or
`key='string value'`.

You can also define that a parameter should have the value of another snippet. That way
you can insert a snippet into another snippet via a parameter. The format of of such
reference is `key -> file/snippet_name`. The referenced snippet should not be a `TEMPLATE` snippet and if it is Pyama will issue
a warning and the snippet will be processed as plain text without macro resolution. 

The values defined this way will be used when resolving the template snippet only at the
very one use where the parameters are defined. They may shadow globally defined keys
assigning different values to them, but they do not overwrite them.

To see a real life example of such template use have a look at the documentation source of
`javahandler.md` that has almost identical documenation for setters and getters and instead of
copy/pasteing the documentation templating is used.

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
from pyama.snippet import MdSnippetWriter, SnippetReader, SnippetMacro
from pyama.processor import Processor

MD = Configuration().file(".*\\.md$").handler(MdSnippetWriter(),SnippetReader())
PY = Configuration().file(".*\\.py$").handler(SnippetReader())
JAVA = Configuration().file(".*\\.java$").handler(SnippetReader(),SnippetMacro())
configs = [MD, PY, JAVA]

Processor(configs, "**/*.*").process()
```

In the example above an `MsSnippetWriter` object and a `SnippetReader` object handles the
markdown files and another `SnippetReader` object handles the Python files. Since the snippets
are stored in a global variable in the snippet handler this work fine, though it would be
cleaner to use a single instance of `SnippetReader`.

The rest of the script is the same as in any other cases. 
