# License Handler

This handler inserts a license text to the start of all the files it is configured for. If the license
text is already there then it replaces the old license text with the new text if there was any change
in the license text.

In addition to the usual configuration license handler itself has to be configured. It should
know where the license file is. It can be done invoking the method `license()` of the
`LicenseHandler` object. If this is not invoked the default configuration is to use the
file `LICENSE.txt` from the current working directory. This file is explicitly configured
in the following sample, which is the test file of the handler in the pyama project. 

[//]: # (USE SNIPPET */license_handler)
```python
        licensehandler = LicenseHandler()
        licensehandler.license("LICENSE.txt")
        JAVA = Configuration() \
            .file(".*\\.java") \
            .handler(JavaHandler(),licensehandler)

        configs = [JAVA]
        processor = Processor(configs, "../test/*.java")
        processor.process()
```

The recommended use is to put the license text int he root directory of the project into the
file `LICENSE.txt` and use the default configuration.

The license handler can work Java and Python files and can be taught to work with other files.
To do that the method

[//]: # (USE SNIPPET */licensehandler_type)
```python
    def type(self, regex, matcher, stopper=None, line_nr=0, start=None, middle='', end=None):
        self.filetypes[regex] = {'line_nr': line_nr,
                                 'matcher': matcher,
                                 'stopper': stopper,
                                 'start': start,
                                 'middle': middle,
                                 'end': end}
```

can be used. The arguments are:

* `self` is the handler object, you do not pass this argument, this is implicit

* `regex` is the regular expression that should match the name of the file. It is usually has
 the format `.*\\.xxx$` where `xxx` is the file name extension. It is important to use the `$`
 at the end of the line, to avoid processing files that have extension that only start with the
 charcters `xxx`. For example `.*\\.py` would also process `.pyc` files, which are binary.
 
* `matcher` is the regular expression that starts a license line. In case of the precnfigured Java
it is `^\\s*/\\*|^\\s*\\*|^\\s*\\*/` that matches any line that starts `/*` or `*` or `*/`.
Obviously these are the leading characters of comment lines that license texts are usually in.  
 
* `stopper` is a regular expression. If a line matches this regular expression during searching for
existing license text then the handler will stop searching and will assume that the license text is
not present in the file and will insert the license text at the start (after the line
number `line_nr`). In case of Java it is `package|import|class`. If any of those word can be fonund
on a line then it is assumed that the license is not in the file yet. Note that this is not a problem
if the license contains these words, because this regular expression is used to find the start
of the license text. The first line of the license better does not contain these words. In case of
Python the stopper regular expression is `^\\s+[^#]`, which means any non-empty line that is not
a comment.
 
* `line_nr` is the line number where the license text can start the soonest. This is usually 0
 to signal that the license text is at the start of the file. It can also be 1 is there is a
 `#! /bin/sh` type line at the start.
 
 * `start` is the string that starts the license text. The string given here is prepended to the
 license text as a separate line. In case of Java it is `/*`. The new line is added to the end
 of the string automatically. If this parameter is `None` then no such line is added.
 
 * `middle` the the string that has to be prepended to the individual license text lines. In case
 of Java it is ` * ` (space, star character, space), which is the start of the usual comment line.
 
 * `end` is the string that ends the license text. The string given here is appended to the
 license text as a separate line. In case of Java it is ` */` (space, star character, slash).
The new line is added to the end of the string automatically.
If this parameter is `None` then no such line is added.

The algorithm to find the already present license text is fairly simple. The handler starts to
read the first segment of the file (other segments are ignored) from the line specified by
`line_nr` and tries to find a line that matches a comment line as defined by `matcher`. After it
treats any consecutive line that seems like a comment line to be part of the lincense text.

If it finds such a starting comment, it will be replaced by the license text. If it does not find
anything like that it will insert the license at the line `line_nr`.

It is recommended to use the `--backup` option with this handler.