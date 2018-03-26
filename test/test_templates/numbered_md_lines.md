
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
1. it contains
2. several lines
3. that will be
4. numbered
in various ways
when used
eight
nine
```

bad use, it will number the opening markup line as well
USE SNIPPET ./snippet NUMBER STEP=2
 1. ```bash
 3. this is a snippet
 5. it contains
 7. several lines
 9. that will be
11. numbered
13. in various ways
15. when used
17. eight
19. nine
```

this will already be two chars and still bad
USE SNIPPET ./10_line_snippet NUMBER
 1. ```python
 2. this is a snippet
 3. it contains
 4. several lines
 5. that will be
 6. numbered
 7. in various ways
 8. when used
 9. eight
10. nine
11. ten
```

here we will have single digits
USE SNIPPET ./snippet NUMBER
 1. ```aaaa
 2. this is a snippet
 3. it contains
 4. several lines
 5. that will be
 6. numbered
 7. in various ways
 8. when used
 9. eight
10. nine
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
 1. 01 this is a snippet
 2. 02 it contains
 3. 03 several lines
 4. 04 that will be
 5. 05 numbered
 6. 06 in various ways
 7. 07 when used
 8. 08 eight
 9. 09 nine
10. 11 this is a snippet
11. 12 it contains
12. 13 several lines
13. 14 that will be
14. 15 numbered
15. 16 in various ways
16. 17 when used
17. 18 eight
18. 19 nine
```

here we have two character digits
USE SNIPPET ./snippet NUMBER START=6
 6. ```i
 7. this is a snippet
 8. it contains
 9. several lines
10. that will be
11. numbered
12. in various ways
13. when used
14. eight
15. nine
```

USE SNIPPET ./snippet NUMBER FORMAT="{:>12d}. "
           1. ```7
           2. this is a snippet
           3. it contains
           4. several lines
           5. that will be
           6. numbered
           7. in various ways
           8. when used
           9. eight
          10. nine
```

USE SNIPPET ./snippet NUMBER FORMAT="{0:02X}: " START=9 STEP=2
09: ```8
0B: this is a snippet
0D: it contains
0F: several lines
11: that will be
13: numbered
15: in various ways
17: when used
19: eight
1B: nine
```

text after the snippet use, remains intact

