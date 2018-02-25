# Pyama Architecture

Pyama is a very simple tool. At this very moment it is 341 lines out of which 102 lines are
the segment handlers. speaking about architecture is a bit funny in such a simple tool, but
if you want to write a segment handler at least the basic terminology and "what is what" has
to be understood.

## Files

Pyama collects a list of files that it will process. The first argument to the `Processor`
as you could see in the listing of `run.py` program is a pattern. The 
`pyama.collector.FileCollector` class will collect the files and filters those that
match some of the regular expressions of the segment handlers. These are the regular
expresion patterns that are configured calling the `.file()` method on the configuration.

Let's copy here the file `run.py` of this project:

[//]: # (USE SNIPPET run.py/run_py)
```python
from pyama.configuration import Configuration
from pyama.snippet import MdSnippetWriter, SnippetReader
from pyama.processor import Processor


MD = Configuration().file(".*\\.md$").handler(MdSnippetWriter())
PY = Configuration().file(".*\\.py$").handler(SnippetReader())

configs = [MD,PY]
Processor(configs, "**/*.*").process()
``` 

The list of files is every file recursively as defined by the pattern `**/*.*` and then 
only those file names are kept in the list that match either `.*\\.md$` ir `.*\\.py$`.
(The `$` at the end is important to exclude extensions that only start with these letters.
For example files with `.pyc` extensions are binary and cause hard time to pyama.)

After the list of the files is collected pyama reads the file.

## File Reading

When a file is read it is spit up into segments. The starts of a segment is a line that 
matches some regular expression. The segment handlers define a method called
`start()` that simply returns the regular expression that matches a source code line
that starts a segment. Pyama uses all the regular expressions that are defined by the
configured segment handlers and if any matches the actual line it starts a new segment.

The regular expression can define a matching group that will be used as the name of the
segment. The name may be referenced by other segments as we already discussed in the
readme.

The segment handlers also define a method named `end()` that returns a regular expression.
A line that matches this regular expression afther the segment matched by the regular
expression returned by `start()` will signal the end of the segment.

Note that the starting and the terminating lines are part of the segments.

When there is a line in the code that does not belong to any named segment then it will be
put into a new segment. Consecustive such lines get into the same segment. Those segments
as well as those, who do not define a name are numbered. Their name will be "0", "1" and
so on. These names should not generally be used.

At the end of the reading phase pyama has several files in the memory each chpped up into
segments.

## Handler executions

Pyama exeutes the handlers several times. It does several passes. In each pass it
goes through all the handlers that are configured and if the actual handler is
configured to be executed in the actual pass then it is executed for each segment
in each file. The code that actually does this is included here:
 
[//]: # (USE SNIPPET */runhandlers)
```python
    def run_handlers(self):
        for pass_nr in range(1, self.passes + 1):
            for handler in self.handlers:
                if pass_nr in handler.passes():
                    for file in self.files:
                        for segment in file.segments:
                            handler.handle(pass_nr, segment)

```

The handlers define a method `passes()` that return a list of numbers including the passes
when they have to be included. This is a fairly general approach. Usually the number of
passes is two. In the first pass the handlers collect information from the files. During
the second pass some of the handlers modify some of the segments of some of the files.

## Wiring the files

After the execution of all the handlers pyama writes the files that were cahnged.

Be careful especially when you execute some segment handlers that were not fully tested
before. Before executing pyama commit all changes to the repo and check the result.

Read on about [segment handlers](segmenthandlers.md)