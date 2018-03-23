# ShellSnippet runs external program

The `ShellSnippet` can execute operating system commands and insert the generated
output into a snippet that can later be used by the snippet handler to insert into any
segments. Originally it was developed as a demonstration and to handle the
Pyama help screen insertion into the `README.md` documentation file.

This segment handler will process segments that start with the line containing

```bash
EXECUTE FOR SNIPPET snippet_name
```

end end with the usual snippet ending line containing

```bash
END SNIPPET
```

The handler uses the inner lines of the segment as a shell command arguments
and executes the external program. The standard output of the program will be
stored as the body of the snippet and can be used by `SnippetWriter` or
`MdSnippetWriter`.

If the operating system is Windows then the `cmd.exe /C` prefix is used to
execute the command. This will make the use of this segment handler
more portable.

This segment handler does not modify any of the segments, it just runs the
code and stores the output in the named segment and makes it available
for the snippet writers.

## WARNING

Use this segment handler with great care. Never execute any Pyama `pyama.py` on project
code you do not trust and which uses this segment handler.