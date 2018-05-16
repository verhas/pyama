# Pyama

Pyama is a command line automated editor that performs some of the tasks that are
otherwise performed manually using some editors. It can be used to modify text
source files in any programming languages inserting or updating boilerplate code.

Modifying the source code programmatically is usually not a good practice. Don't do
that if it is possible. Pyama is a practical tool to amend the code editing workflow.
If you have to generate code, it means that your development process is not optimal.
The reason can be the insufficiency of some of the tools. For example, you generate
getters and setters into the source code, because Java does not
generate automatically the setters and getters during compilation time. But getters and
setters are generated by any editors, that is simple. Unless you forget to regenerate when you
change the code.

## Sample Problems Needing Pyama

### Creating setters, getters, constructor, hashCode, toString, equals...

These are code fragments that are generated most of the time. These are so general problems and 
they are needed to be generated for Java programs that even the IDEs support the generation of
these methods.

The issue using the IDE is that you can forget to update your class after you modified the fields.

Pyama has a built-in Java handler that can generate these and more and even if you forgot to
regenerate one of the hashCode or toString of some of the classes you modified Pyama will
regenerate them all when you run it. If you forget to run Pyama altogether that is a problem
Nevertheless, it is much easier to run a command line tool once than remembering what classes
you changed and ask the IDE one by one to regenerate the code.

In addition to the code that IDEs can generate Pyama can also generate a nested builder class,
and we plan to add arbitrary code generation without Python coding via templates.

### Converting object to Map and back

I faced other issues that are almost as simple as generating setters and getters, but being
specific they are not supported by the IDE. I had many Java classes that I needed to
convert to `Map` and from `Map` to object. The general solution would have been to 
create a reflection tool that reads the fields of the object and generates the `Map`
and another that reads the values from the `Map` and wrote the fields of the object.
For some technical reasons (some of which could have been coped with though) using
reflection was not an option. We ended up hand-coding the back and forth conversions.
(Also know that I simplified the issue, the real-life problem was more complex.) 


### Include code snippets to documentation

Another issue I faced during my practice is that most of the markup languages do not
allow to include a snippet from other source files. For example, using markdown
you can have some sample code like the following:

[//]: # (USE SNIPPET pyama.py/run_py SKIPPER)
```python
from pyama.configuration import Configuration
from pyama.lineskipperhandler import LineSkipper
from pyama.processor import Processor
from pyama.regexhandler import RegexHandler
from pyama.shellsnippet import ShellSnippet
from pyama.snippet import MdSnippetWriter, SnippetReader, SnippetMacro

snippetWriter = MdSnippetWriter()
MD = Configuration().file(r".*\.md$").handler(snippetWriter, SnippetReader(), LineSkipper())
SEGMENT = Configuration().file(r".*\.md$").exclude(r"regexhandler\.md").handler(RegexHandler())
PY = Configuration().file(r".*\.py$").handler(SnippetReader(), ShellSnippet())
JAVA = Configuration().file(r".*\.java$").handler(SnippetReader(), SnippetMacro())
configs = [MD, PY, JAVA, SEGMENT]

Processor(configs, "**/*.*").process()
``` 

I wanted to have these code fragments copied from the source code, usually from
unit test files. Whenever the unit test changed it had to be copied to the documentation.

The first solution was to use some existing macro tool that processed an "extended"
markdown file and generated the markdown. Then I faced that the editors that show the
markdown WYSIWYG could not cope with the file that still needed preprocessing. The file
name extension I used was not `.md` to separate the markdown files that needed preprocessing
from those that were native markdown. If I wanted to have the files available on the GitHub
web interface then I had to store them in the source directory and then the generated and
the "real" source files got mixed. If they get mixed in a directory then there is no point
to separate them into separate files.

The other approach is to accept the fact that some part of the source file is copied and
generated and instead of trying to separate the source from any generated we try to automate
the boilerplate code generation and the copy paste. Pyama does that. It automates the boilerplate
generation and can copy parts of the source into other source files.

## What is Pyama

Pyama will process your source files and if there is some modification that induces modification
needs in other parts of the source code it automatically will change the code. It will copy part
of some source files (probably code files) into other source files (probably documentation).

It will also generate Java class setters, getters, constructors, equals, hashCode, toString and
builder pattern out of the box.

It will execute your small Python written handlers that you can code to generate code other than
the prefabricated Java code generators. To do this Pyama provides simple API and simple SPI
to implement in your handlers. All you need to focus is to generate the code from the available
information, Pyama will do the rest: reading the file, file the segments that need modification,
write back the result if there was any change.

## How Pyama works

Pyama reads a set of files, extracts information from these files and then selects some
of the files and overwrites some part of those files.

The configuration is done using fluent API as you could already see in the sample above.
You define file name patterns and handers.

Pyama reads the files that are configured and splits the read text into segments. The
segments start with special lines as defined by the handlers. Different handlers may
define different segment start and segment end patterns.

When all the text are in segments in the memory then Pyama invokes the different handlers
in several rounds letting them collect information from the text segments and also to
modify the individual segments.

After this phase, Pyama writes the files where one or more segment was changed.

This structure is very general and the specific tasks are implemented in the handlers.

## Use of Pyama

Typically you will install Pyama into your development environment and you create a `pyama.py`
file in your development root directory. You can name it any way you want btw. It will
be an extremely simple Python source file. The actual `pyama.py` of this project you can
see above.

Yes, it was copied into this markdown file using Pyama. This little program declares the
configuration that, in this case, says we are using markdown and python source files and
we define two segment handlers. We will discuss them later. They need a bit of python
knowledge but Pyama is designed so that it is extremely easy to create segment handlers.

After the declaration of the file types and how we want to handle them, we invoke the
Pyama processor and generally that is it. Pyama reads all the files that match `**/*.*`
and calls the handlers to do their work. `SnippetReader` is written to read the
code fragments from the python source files and `MdSnippetWriter` is written
to modify the markdown files where it has to copy some of the code fragments
the other segment handler collected before.

Snippet segments in Python start with the line

```python
# START SNIPPET run_py
``` 

and the end of the segment is

```python
# END SNIPPET
```

If other handlers also work with the Python files then they may define a different segment
starting and segment ending patterns.

The `run_py` is the name of the snippet. The `SnippetReader` will copy the lines between
the start and end line into the memory and when `MdSnippetWriter` is executed it will
be available in a python dictionary.

Similarly, snippet segments in the markdown files start with 

```
[//]: # (USE SNIPPET pyama.py/run__py)
```

and ends with a line that contains only three backticks. The keywords `USE SNIPPET` tell
Pyama to start a new segment and the `pyama.py/run_py` tells the segment handler
`MdSnippetWriter` that it has to replace the content of the segment as it is now
to the snippet that came from the file `pyama.py` and is named `run_py`. (Note that in the
sample above I had to replace `run_py` with `run__py` otherwise Pyama was recognizing
it as something it should process.)

## Command line options

[//]: # (USE SNIPPET pyama.py/run_output)
```bash
usage: pyama.py [-h] [-l LEVEL] [-n] [-b] [-f LOGFILE]

optional arguments:
  -h, --help            show this help message and exit
  -l LEVEL, --level LEVEL
                        set the logging level explicitly DEBUG, INFO, WARNING,
                        ERROR or CRITICAL
  -n, --dry             do not write the changes back to the files
  -b, --backup          create .BAK for changed files
  -f LOGFILE, --logfile LOGFILE
                        specify log file
```

## Precooked handlers

Pyama comes with an ever-expanding list of pre-cooked handlers. These are

* [snippet handler](./doc/snippet.md) can recognize code snippets in program source files
  and can copy these into documentation files (especially into markdown files)

* [shell snippet handler](./doc/shellsnippet.md) can executes external program and
  use the output of the code as snippet

* [javahandler](./doc/javahandler.md) can create constructors, setters, getters, `equals`
  and `hashCode` methods as well as `toString` and nested builder class in Java classes.

* [licensehandler](./doc/licensehandler.md) can check that each file has a license text
  at the start of it and inserts the license text if it was not there or updates the text
  if it changed in a separate sample license file

* [linenumberer](./doc/linenumberer.md) can put line numbers on lines in snippets
 
* [regexhandler](./doc/regexhandler.md) can execute regukar expression search and replace on
  snippet lines 

* [line skipper](./doc/lineskipper.md) can remove certain lines from the segment making it possible
  to exclude certain lines from snippets.

## More documentation

If you have the segment handlers and can run python code and you are satisfied then
there is no point to read on. The application can be installed with minimal python
infrastructure knowledge and the `pyama.py` can easily be created without really
understanding python.

However, if you need something that is not available and you want to write segment handler(s)
then go on.

* [Architecture, structure of pyama](./doc/architecture.md)
* [Writing segment handlers](./doc/segmenthandlers.md)