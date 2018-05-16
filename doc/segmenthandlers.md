# Pyama Segment Handlers

Segment handlers are small Pyathon classes that are inviked by pyama. Recall that after
reading all the files and splitting them into segments pyama invokes all configured
segment handlers a few times in passes. Pyama invokes a handler if the handler claims that it can
do something in that specific pass and there is an invocation for each segment in
each file.

Segment handlers can collect information reading from the segments and can modify the
segments. The modifications will be written back to the file.

A segment handler is best written extending the `pyama.segmenthandler.SegmentHandler`
class. This class is the following:


[//]: # (USE SNIPPET */segmenthandler_py)
```python
class SegmentHandler:
    def passes(self):
        '''
        :return: the numbers of passes when the handler needs to be invoked. Passes are numbered from 1 upward.
        '''
        return [1]

    def start(self):
        '''
        :return: the regular expression to be used to recognize the start of a segment handled by this segment handler
        '''
        return None

    def end(self):
        '''
        :return: the regular expression to be used to recognize the end of a segment handled by this segment handler,
        or None if there is no such regular expression
        '''
        return None

    def handle(self, pass_nr, segment):
```

The methods here are supposed to be overridden.

* `passes()` should return the list of integers that list the passes in which the handler
is to be invoked. The `SegmentHandler` implementation returns `[1]` that means that the
handler should only be invoked during the first pass.

*  `start()` should return a regular expression that is used to locate the start of a
segment.

* `end()` should return the regular expression that is used to locate the end of the 
segment that started with the line that matched the regular expression returned 
by `start()`.

* `handle()` is invoked by pyama during the execution of the handlers.

We will look at how to implement these methods.

## `passes`

The implementation of this method usually a simple `return [a,b,c]` format statement
that simply list the numbers of the passes that the handler should be invoked. If the
handler is to be invoked only during the first pass then the method should
`return [1]`. If the handler is to be invoked only during the second pass then the
method should `return [2]`. If it is to be invoked in both passes then the method
should `return [1,2]`.

There is no limit for the number of passes, though it is not likely that a real handler
would need more than a few passes. Usually there is a reading and information gathering
pass, the first one and there is one pass that modifies the segments.

There is a valid use case to use more than two passes when there is some dependency
between different handlers and some handler has to be invoked before the other. In
such situation the handler supposed to run sooner may ask for a lower pass number and
the one depending on the other one a larger pass number.

Pyama is taking the maximum of all passes returned by all handlers and executes that
many passes. It does not skip passes that are not needed by any handler, thus it is
recommended to use small integers as pass numbers.

It is also recommended to implement the constructor of the handler accepting a named
argument `runpass` that defaults to the list of passes. That way the configuration code
may decide which handler to run in which pass depending on which are used at all.

For example you may use the snippet handler in pass 1 and 2. Then you use the regular expression
handler to delete some line numbers from some segments that are maintained manually. This
handler runs in pass 3. After that in pass 4 you may want to run the line numbering
handler. On the other hand if you do not use the regular expression handler to delete the
line numbers, or at all, then you can run the numbering in pass 3.

## `start`

The implementation of this method is usually a simple `return str` statement that
returns a string contsant containing the regular expression to match the start of a
segment.

The class `SnippetReader` defines the regular expression as a string

```python
r'START\s+SNIPPET\s+(\w[\w\d_]*)'
```

Note that this regular expression can be used to identify snippet starts in Python,
Java or practically any other programming language. In Python the start will actually
look 

```python
# SNIPPET START mySnippet
```

and the same time the snippet start in Java will be

```java
// SNIPPET START mySnippet
```

Usually there is no reason to write different handlers for different program language
snippets, especially not for reading purposes. Pyama invokes all the handlers for all
the segments. Even if we created different handlers to read snippets from Java and
Python files pyama would call each of them, no matter which handler's `start()`
regular expression matches the start of the segment.

Handlers, if needed, should check against their regular expressions the first line
of the segment they are processing.

The regular expression may also locate the name of the segment. The name will be the
first matching group, as returned by `match.group(1)` after the line matched the
regular expression. This is essentially the part of the regular expression between the
parentheses.

Also note that there is no restrictions imposed by pyama about the name of the segment.
The name of the segment is just a string for pyama. The segment handling routines and
regular expressions impose restrictions if they have to. In case of the "sample"
`SnippetReader` class the regular expression returned by the `start()` method
says that the name of the segment can be anything that starts with a letter and
optionally continues with letters, numbers and underscore characters.

When a segment does not define anything there is no need to have parentheses to define a
name. In that case the name of the segment will be generated automatically. It will be a
string that is a decimal number starting from "0" in each file and is incremented for
each new unnamed segment. Segments are also named if the regular expression matching
results an empty string as name, as we will see below.

The same `start()` expression may need to be used to extract some of the
parameters. For example the class `SnippetWriter` defines the start regular
expression as

```python
r'USE\s+SNIPPET(.{0})\s+([\w\d_/\.\*]+)'
```

In this case there is no need for a name, but the handler itself needs some parameters.
This second parameter is the name of the snipped that is used in this segment. `SnippetWriter`
will actually update the content of the segment using this snippet, which was created during the
first pass by `SnippetReader`. Handling the name of the referenced snippet is the responsibility
of the `SnippetWriter`, but it is designed to use the same string as regular expression which is
returned by `start()`.

The `(.{0})` in the above string returned by `start()` matches a zero length string and although
in this case there is a first matching group the segment is numbered instead of using an empty
string as a name.

An alternative possibility for `SnippetWriter` could have been to use two regular expressions: one for
identifying the start of the segment and another to extract parameter inside the handler,
which is the name of the referenced snippet.

## `end()`

The implementation of this method is usually a simple `return str` statement that
returns a string constant containing the regular expression to match the end of a
segment that was started finding a matching line for the regular expression returned by
`start()`.

Note that these regular expressions are handled totally different from `start()` regular
expressions. When trying to find the start of a segment each regular expression returned
by the different `start()` methods of the handlers are consulted. When a segment started,
on the other hand, only the one regular expression returned by the `end()` method of the
handler of which `start()` was matching is used.

So if a handler's `start()` regular expression was used to start a segment it may
not be accidentally terminated by another handlers `end()` regular expression.

Note that both `start()` and `end()` are invoked only during configuration. They are
supposed to be idempotent but generally they are invoked only once and the result
string is used later.

## `handle()`

This is the method that has to handle the segment. This method is invoked for each pass
the handler signals interest for each segment in each file, for which the handler is configured.

The method gets two arguments, `pass_nr` and `segment`. The first argument is the actual number of
the pass starting with 1 and incremented for each pass. The second argument is the segment that
the handler has to work on for this invocation.

The structure of a segment is defined in the class `pyama.file.Segment`:

[//]: # (USE SNIPPET */segment_structure TRIM)
```python
self.name = name
self.filename = filename
self.text = []
self.next = None
self.previous = None
self.modified = False
self.parameters = {}
```

The `name` is the name of the segment as defined in the snippet starting line or "0", "1",
and so on if the segment is numbered. Pyama does not care the uniqueness of the segment names.
It is up to the handlers how they manage name collisions. For example the handler
implemented in the class `pyama.snippet.SnippetReader` concatenates the snippets that come from
different segments having the same name.

The `filename` is the full path name of the file that was used to open the file for reading
that contains the segment. It can be used by the handler to avoid handling files that
it cannot handle. If there is, for example, a handler that can handle only Python files
then this field can be used to ensure to manage only segments that belong to a file that
has `.py` extension. It is note however that the configuring code should configure the
handler not to be invoked for such a file.

The `text` contains the lines of the segments. Each source line includes the terminating
new line, if there is any. (The last line in the file may not contain one.)

The fields `next` and `previous` link the segments together within one file and they are
available for the handlers if the want to traverse the segments in a single invocation.

The field `modified` SHOULD be set to `True` if the handler modified the segment. Pyama
writes back changes to the files only for files that have at least one segment with
this field set to `True`. (Pyama also checks that the files are really changed and
does not overwrite a file with identical content.)

To see two examples we will look at the implementation of the `handler()` method of the
classes `SnippetWriter` and the class `MdSnippetWriter`.

### `SnippetWriter.handle()`

[//]: # (USE SNIPPET */SnippetWriter_handle TRIM)
```python
def handle(self, pass_nr, segment):
    startline = segment.text[0]
    match = re.search(SnippetWriter.start_line, startline)
    if not match:
        return
    text = self.get_modified_text(match.group(2), segment)
    if not text:
        return
    text = self.chomp(text, False)
    segment.text = [segment.text[0]] + text[1:-1] + [segment.text[-1]]
    segment.modified = True
```

The handler first fetches the first line of the segment and checks that it matches its
`start()` regular expression. This also serves the purpose to get the referenced snippet
from the line looking at the second matching group.

The private method `get_modified_text()` method looks up the snippet in the dictionary
that was built up in the previous pass by the class `SnippetReader`. If there is some text found
in the dictionary then it modifies the segment lines.

The handler is careful to keep the original first line of the segment because it has to find it again when 
it is executed again. Also the last line that terminates the segment is preserved.

The new lines between these two lines are the text from the other segment that was referenced.
Note that the first and the last line of the source segment, which gets copied here are removed. They
are not needed here. We only need the the code sample.

The last action when the segment is modified is to signal the modification setting the `modified` field
to `True`.

### `MdSnippetWriter.handle()`

[//]: # (USE SNIPPET */MdSnippetWriter_handle TRIM)
```python
def handle(self, pass_nr, segment: Segment):
    startline = segment.text[0]
    match = re.search(SnippetWriter.start_line, startline)
    if not match:
        return
    text = self.get_modified_text(match.group(2), segment)
    if not text:
        return
    if len(segment.text) < 2:
        logger.warning("segment %s/%s is too short, cannot be processed" % (segment.filename, segment.name))
    else:
        text = self.chomp(text, False)
        segment.text = [segment.text[0], segment.text[1]] + \
                       text[1:-1] + \
                       [segment.text[-1]]
        segment.modified = True
```

The class `MdSnippetWriter` extends the class `SnippetWriter` thus it has access to the same "private" methods.
The only difference is that it keeps not only the first but
also the second line of the original segment. It is because the first line is the 
one that signals the start of the snippet use and the second line is the three back ticks that starts the
markdown code listing.

The final statement is signalling the modification of the segment.