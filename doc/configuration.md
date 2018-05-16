# Pyama configuration

To start Pyama you have to create a `Processor` object in the main script and then
start the processing invoking the argumentess `process()` method. To create a `Processor`
object you have to import the class

```
from pyama.processor import Processor
```

and invoke the constructor

```
Processor(configs, "**/*.*").process()
```

The first argument is the list of the configuration objects. We will look at how to create that
list soon. The second argument is a file name pattern used to collect all the files
that the processor will process. When it starts with `**` it means that the directories
recursively will be processed. This argument is actually passed on to the built-in python `glob()`
method, see the documentation of that method for further information on how this parameter is
interpreted.

The first parameter `configs` contains the configurations. Each configuration can be created using
the `Configuration` object. To do that the code has to import the class

```
from pyama.configuration import Configuration
```

and can create one or moe configuration calling the constructor of the class one or more times.

The constructor has no parameters, but the class contains configuration methods that can be invoked
in a method-chain style. The line, for example, that specifies in `pyama.py` what files are to be
processed using the regular expression handler is the following:

```
SEGMENT = Configuration().file(r".*\.md$").exclude(r"regexhandler\.md").handler(RegexHandler())
```

The method `file()` specifies a regular expression pattern of the file names that are to be processed
by this handler. `exclude()` can exclude some of the files. `handler()` defines one or more
handlers.

Note that the regular expressions in the argument of `file()` and `exclude()` are applied to the
file names that were already collected by the processor. If the file pattern passed as an argument
to `Processor(configs,pattern)` does not collect a file then it will not be in the list of the
files that are processed and will not be processed.

A file is processed by a handler if the handler object is passed as an argument to the method `handler()`,
the name of the file matches at least one of the regular expressions that are passed to the method
`file()` and does not match any of the regular expressions that are passed to `exclude()`.

A handler object can be passed more than one time to the method `handler()` and it still will be invoked
only once. Different instances of the same handler class are not treated as the same, they will be invoked
separately.

The processor will invoke a handler if there is at least one configuration passed to the `Processor()`
constructor that says it has to be invoked. In other words if a file name matches a regular
expression passed the `exclude()` but another configuration does not exclude that file for the same
handler instance then the handler instance will be in use.