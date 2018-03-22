
START SNIPPET snippet
this is a snippet
it contains
several lines
that will be
numbered
in various ways
when used
eight
nine
END SNIPPET

START SNIPPET 10_line_snippet
this is a snippet
it contains
several lines
that will be
numbered
in various ways
when used
eight
nine
ten
END SNIPPET

USE SNIPPET ./snippet NUMBER LINES=3:7
```java
this is a snippet
it contains
several lines
that will be
numbered
in various ways
when used
eight
nine
```

bad use, it will number the opening markup line as well
USE SNIPPET ./snippet NUMBER STEP=2
 1. ```bash
this is a snippet
it contains
several lines
that will be
numbered
in various ways
when used
eight
nine
```

this will already be two chars and still bad
USE SNIPPET ./10_line_snippet NUMBER
 1. ```python
this is a snippet
it contains
several lines
that will be
numbered
in various ways
when used
eight
nine
ten
```

here we will have single digits
USE SNIPPET ./snippet NUMBER
 1. ```aaaa
this is a snippet
it contains
several lines
that will be
numbered
in various ways
when used
eight
nine
```

START SNIPPET long_snip
01 this is a snippet
02 it contains
03 several lines
04 that will be
05 numbered
06 in various ways
07 when used
08 eight
09 nine
11 this is a snippet
12 it contains
13 several lines
14 that will be
15 numbered
16 in various ways
17 when used
18 eight
19 nine
END SNIPPET

here we will have two character by default with space at the start
USE SNIPPET ./long_snip NUMBER LINES=2:
```z
01 this is a snippet
02 it contains
03 several lines
04 that will be
05 numbered
06 in various ways
07 when used
08 eight
09 nine
11 this is a snippet
12 it contains
13 several lines
14 that will be
15 numbered
16 in various ways
17 when used
18 eight
19 nine
```

here we have two character digits
USE SNIPPET ./snippet NUMBER START=6
 6. ```i
this is a snippet
it contains
several lines
that will be
numbered
in various ways
when used
eight
nine
```

USE SNIPPET ./snippet NUMBER FORMAT="{:>12d}. "
           1. ```7
this is a snippet
it contains
several lines
that will be
numbered
in various ways
when used
eight
nine
```

USE SNIPPET ./snippet NUMBER FORMAT="{0:02X}: " START=9 STEP=2
09: ```8
this is a snippet
it contains
several lines
that will be
numbered
in various ways
when used
eight
nine
```

text after the snippet use, remains intact

