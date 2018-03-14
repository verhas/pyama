# ShellSnippet runs external program

The `ShellSnippet` segment handler was developed as a demonstration and to handle the
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

If the operating system is some `win` platform arguments are prepended with two
more arguments, `cmd.exe` and `/C`. This will make the use of this segment handler
more portable.

This segment handler does not modify any of the segments.

## WARNING

Use this segment handler with great care. Never execute any Pyama run on project
code you do not trust and which uses this segment handler.