# Pyama Segment Handlers

Segment handlers are small Pyathon classes that are inviked by pyama. Recall that after
reading all the files and splitting them into segments pyama invokes all configured
segment handlers a few times in passes. It invokes a handler if it claims that it can
do something that that specific pass and there is an invocation for wach segment in
each file.

Segment handlers can collect information reading from the segments and can modify the
segments. The modifications will be written back to the file.

A segment handler is bets written extending the `pyama.segmenthandler.SegmentHandler`
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
        pass
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
` return [1]`. If the handler is to be invoked only during the second pass then the
method should `return [2]`. If it is to be invoked in both passes then the method
should `return [1,2]`.

There is no limit for the number of passes, though it is not likely that a real hander
would need more than two passes. Usually there is a reading and information gathering
pass, the first one and there is one pass that modifies the segments.

There is a valid use case to use more than two passes when there is some dpeendency
between different handlers and some handler has to be invoked before the other. In
such situation the handler supposed to run suuner may ask for a lower pass number and
the one depending on the other one a larger pass number.

Pyama is taking the maximum of all passes returned by all handlers and executes that
many passes. If does not skip passes that are not needed by any handler, thus it is
recommended to use small integers as pass numbers.

## `start`

The implementation of this method is usually a simple `return str` statement that
returns a string contsant containing the regular expression to match the start of a
segment.

The class `SnippetReader` defines the regular expression as a string

```python
'START\\s+SNIPPET\\s+(\\w[\\w\\d_]*)'
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
Python files pyama would call each of them, no matter which hander's `start()`
regular expression matches the start of the segment.

If handlers, if needed, should check against their regular expressions the first line
of the segment they are processing.

Also note that there is no restrictions imposed by pyama about the name of the snippet.
The name of the snippet is just a string for pyama. The snippedt handling routines and
regular expressions impose restrictions if they have to. In case of the "sample"
`SnippetReader` class the regular expression returned by the `start()` method
says that the name of the snippet can be anything that starts with a letter and
optionally continues with letters, numbers and underscore characters.

## `end()`

The implementation of this method is usually a simple `return str` statement that
returns a string contsant containing the regular expression to match the end of a
segment that was started finding a matching line for the regular expression returned by
`start()`.

Note that these regular expressions are handled totally different from `start()` regular
expressions. When trying to find the start of a segment each regular expression returned
by the different `start()` methods of the handlers are consulted. When a segment started,
on the other hand, only the one regular expression returned by the `end()` method of the
handler of which `start()` was matching is used.

So if a handler's `start()` regular expression was used to start a segment it may
not be accidentally terminated by another handlers `end()` regular expression.

## `handle()`

This is the method that has to handle the segment. This method is invoked for each pass
the handler signals interest for each segment in each file. 

The structure of a segment is defined in the class `pyama.file.Segment`:

[//]: # (USE SNIPPET */segment_structure)
```python

```

 
