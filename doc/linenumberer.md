# Line numbering handler

The line numbering handler is a very simple one. It numbers the lines of the segment
if the first line of the segment contains 

```bash
NUMBER
```

It also processes two arguments of the form

```bash
NUMBER START=1 STEP=1 FORMAT="{:d}. LINES=n:m"
```

Both `START` and `FORMAT` are optional.


Using `START` you can define the start value where the line 
numbering starts. The value following the
keyword `START` has to be an unsigned positive integer.

Using `STEP` you can define the step value between the 
line numbers. The value following the
keyword `STEP` has to be an unsigned positive integer.

Using `FORMAT` you can define the format of the number.
The default is to use the decimal format of the
line number followed by a dot and a space. If the snippet is less than 10 lines
then a single digit. If the snippet is more than 10 lines, or the numbering starts
so that the last line number is greater than 9 then the default format is
two digits for numbers larger than 9 and one digit with a leading space for 1 to 9.
The format string should be enclosed between
`"` or `'` (double or single quote) characters. The format string is used through the
standard Python string `format()` method. For the various possibilities see 
[the Python documentation](https://docs.python.org/3.4/library/string.html#grammar-token-format_spec).

Using `LINES` you can define start and end line that is numbered. The other lines will
not be numbered. The numbers `n` and `m` can be positive or negative. If any of it is negative then
it is an index from the end of the lines. This is indexing the same style as Python uses indices.
If either `m` or `n` is missing the default value will be the first and the last line
respectively. Specifying `LINES=:` is the same as not specifying any `LINES` parameter. The
second parameter `m` is the index of the line that is already not numbered. In other words
lines with index `i` for which `n` <= `i` < `m` stands.

The `LINES` parameter is usually used together with the markdown snippet writer where the second
line of the snippet is starting the code sample and remains intact. This should also be
followed by the numbering if used. In this case the parameter `LINE=2:` will
protect the line that starts the code display starting. 

The line numbering handler is usually used together with the snippet handler
using the format

```bash
USE SNIPPET */whatever_my_snippet NUMBER START=1 STEP=1 FORMAT="{:d}. "
```

to insert the numbering.

The line numbering handler runs by default during the third pass ensuring that the
snippet using segments were already overwritten with the lines of the snippets. If
you use other handlers and you want to run the handler in a different pass then
use the optional argument `runpass` when creating the handler instance in the
configuration code. The value to `runpass` is the list of the passes in which
the handler has to be invoked.
