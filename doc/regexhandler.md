# Regular Expression Handler

The regular expression handler can be used to execute regular expression based
search and replace on the lines of a segment and to delete lines from a segment.
This handler does not define any segment delimiter. It has to be used with
som other handler. Typically it is used together with the snippet handler in the
third pass after the snippets were updated in the segments.

## Sample Use

It can be used, for example, to delete the line leading ` * ` characters if some
snippets are fetched from JavaDoc.

Another example is to run the regular expression handler in a pass to remove the
numbers from the start of the lines in a segment and run the line numbering
handler in the next pass to insert the numbers, that may have been crippled 
during editing. This way you need not manually edit all the numbers of numbered
lines when you delete or insert a line. You can have a segment that looks like
the following after some editing:

```bash
START SNIPPET numbered NUMBER START=10 STEP=10 FORMAT=" {:2d} " REPLACE "^\s*\d+\s*" -> ""
 1 this way we
 2 can renumber
even if we inserted lines or the numbering
 3 the lines
is totally got wrong...
END SNIPPET
```

It will be transformed to be

```bash
START SNIPPET numbered NUMBER START=10 STEP=10 FORMAT=" {:2d} " REPLACE "^\s*\d+\s*" -> ""
 10 this way we
 20 can renumber
 30 even if we inserted lines or the numbering
 40 the lines
 50 is totally got wrong...
END SNIPPET
```

with the appropriate snippet handler, regular expression handler and line numbering handler.

## Format

The regular expression handler works on a segment if the first line of the
segment contains `KILL` and/or `REPLACE` parameters.

The `KILL` parameter has to be followed by one or more regular expressions enclosed
between `"` or `'` (double or single) quotes. The lines that match any of the expressions
will be removed from the segment.

The `REPLACE` keyword has to be followed by a regular expression, then the `->`
characters and a replacement string. The regular expression and the string
has to be enclosed between `"` or `'` (double or single) quotes. For example
the following segment start

```bash
.... REPLACE "this" -> "that" 'question' -> 'answer'
```

will replace every _this_ to _that_ and every _question_ to _answer_ in the lines
of the segment. In the replacement string you can use `\1`, `\2` and so on to
insert the capture groups of the regular expression.

The check, whether a line has to be killed, is executed before the replacements.

The regular expression handler runs by default during the third pass ensuring that the
snippet using segments were already overwritten with the lines of the snippets. If
you use other handlers and you want to run the handler in a different pass then
use the optional argument `runpass` when creating the handler instance in the
configuration code. The value to `runpass` is the list of the passes in which
the handler has to be invoked.