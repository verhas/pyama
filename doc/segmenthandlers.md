# Pyama Segment Handlers

Segment handlers are small Pyathon classes that are inviked by pyama. Recall that after
reading all the files and splitting them into segments pyama invokes all configured
segment handlers a few times in passes. It invokes a handler if it claims that it can
do something that that specific pass and there is an invocation for wach segment in
each file.

Segment handlers can collect information reading from the segments and can modify the
segments. The modifications will be written back to the file.

[//] # (USE SNIPPET */segmenthandler_py)
```python

```

