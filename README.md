# pyama
pyama is a Python based modular command line text processor.

Pyama can be used to generate and modify text source files in any programming languages.

Modifying the source code programmatically is usually not a good practice. Don't do
that if it is possible. Pyama is a practical tool to amend the code editing workflow.
If you have to generate code, it means that your editing process is not optimal.
The reason can be the insufficiencies of some of the tools. For example you generate
getters and setters into the source code, because Java is an old language and does not
generate automatically the setters and getters during compilation time.

Another issue I faced during my practice is that most of the markup languages do not
allow to include a snippet from other source files. For example usign markdown
you can have some sample code like

[//]: # (This may be the most platform independent comment)
```

``` 

Generating setters and getters is done by the editor. You need pyama when you want   


Even though that
is usually the case many times editors frequently generate code for us (injecting them to 
source files)


