# Java Handler

The Java Handler can be used to automatically generate

* constructors that will get the arguments for the final fields that are not initialized,
* getters and setters for the fields
* `equals` and `hashCode` (only together, you can not generate only one)
* `toString` method.

## FIELDS

Generating getters, setters, `equals()` and `hashCode()` as well as `toString()` need the fields.
WHen using pyama to generate any of the above the fields have to be listed in a segment. Pyama
will collect all the information that it needs later to modify the segments that are the
placeholders for getters, setters and so on.

The listing of the fields should start with a line that contains the string `FIELDS`. This
usually is a comment line like in the sample below.

The fields have to listed on separate lines, as we usually do when we program on Java.
There can be comments following the field declaration on the same line to control the
code generation. The possible comments are discussed when we detail the code generation part,
for now we have here a sample that shows some fields.

[//]: # (USE SNIPPET test/MyClass.java/fields)
```java
    // MATCH (\w*)="(.*)"
    // VERSION="3.13";
    // NO MATCH
    // FIELDS
    private boolean b; // constructor
    static Boolean bObj; // setter getter
    byte by; //package setter package getter
    Object obj; // package getter
    Integer iObj; // no builder
    int i; // 3.13
    long l;
    Long lObj;
    char c;
    Character cObj;  // builder method "separator"
    float f;
    Float fObj;
    short s;
    Short sObj;
    Double dObj;
    final double d;
    // END
```

The end of the segment is signalled with a line that contains the string `END`. All other segments
also end with a line that contains the string `END`.

The FIELDS segment is input segment, the handler does not modify it, it uses this segment to gather
information during execution.

This segment has to precede the other segments that this handler works with. 

## CONSTRUCTOR

The constructor segment starts with a line containing `CONSTRUCTOR` and ends with a line containing
`END`. This segment is overwritten by the handler.

The handler will generate a constructor that initializes all `final` fields that do not get value
on the line where they are declared and those fields that have the string `constructor` on the
line where they are declared. In the sample above the fields `d` is included because it is
`final`, no value was assigned to it and it is not `static`. The field `b` is included because 
it has a comment that says it has to be included no matter what. Note that if there is a
`// constructor` comment on a field declaration line for a field that is `final` and `static` the
pyama will generate a constructor that will not compile. Pyama is mainly based on regular
expressions, string handling and it does not analyze Java code.

You can slightly modify the generated constructor and Pyama may keep the changes. You can change the
access modifier of the constructor and Pyama will consider than when regenerating the new constructor when
a field has changed. What actually Pyama does is, that it looks at the first line of the segment and if that
segment looks like something like a constructor head (actually matching the regular expression `.*\(.*\).*`
then it will use that line replacing the part between the parentheses with the new parameters. 

[//]: # (USE SNIPPET test/MyClass.java/constructor)
```java
    // CONSTRUCTOR
    public MyClass(final boolean b, final double d){
        this.b = b;
        this.d = d;
    }
    // END
```

The name of the constructor in Java is the same as the name of the class. The handler reads
the segments at the start of the file that declares the class. It looks for a line that has the
keyword `class` followed by space or spaces and an identifier. If you happen to write the
keyword `class` and the name of the class in separate lines that is not only non-java style and
awkward but will also prevent this handler to know the name of the class

The above sample shows the generated constructor for the fields as listed above. 

## GETTERS
<!-- START SNIPPET xetters TEMPLATE
The {xetters} segment starts with a line containing `{XETTERS}` and ends with a line containing
`END`. This segment is overwritten by the handler.

By default pyama will generate {xetters} for those fields that are `private` and not `static`{and_not_final}.
If the segment starting comment contains the string `for all` then pyama will generate {xetters}
for all the fields.

It is also possible to force individual fields to get {xetter} in the generated code. If the
comment following the field contains `{xetter}` then it will get a {xetter}.

If the comment contains `protected {xetter}` then the {xetter} will have `protected` access modifier.
If the comment contains `package {xetter}` then the {xetter} will have no access modifier and as such
it will be package private.

END SNIPPET -->

[//]: # (USE SNIPPET ./xetters WITH xetters="getters" xetter="getter" XETTERS="GETTERS" and_not_final="")

The getters segment starts with a line containing `GETTERS` and ends with a line containing
`END`. This segment is overwritten by the handler.

By default pyama will generate getters for those fields that are `private` and not `static`.
If the segment starting comment contains the string `for all` then pyama will generate getters
for all the fields.

It is also possible to force individual fields to get getter in the generated code. If the
comment following the field contains `getter` then it will get a getter.

If the comment contains `protected getter` then the getter will have `protected` access modifier.
If the comment contains `package getter` then the getter will have no access modifier and as such
it will be package private.

[//]: # (END SNIPPET)

For `boolean` and `Boolean` fields the name of the getter will be `isXxxx()`, for other fields
it is `getXxxx()`.

[//]: # (USE SNIPPET test/MyClass.java/getters)
```java
    // GETTERS for all
    public boolean isB(){
        return this.b;
    }
    public Boolean isBObj(){
        return this.bObj;
    }
    byte getBy(){
        return this.by;
    }
    Object getObj(){
        return this.obj;
    }
    public Integer getIObj(){
        return this.iObj;
    }
    public int getI(){
        return this.i;
    }
    public long getL(){
        return this.l;
    }
    public Long getLObj(){
        return this.lObj;
    }
    public char getC(){
        return this.c;
    }
    public Character getCObj(){
        return this.cObj;
    }
    public float getF(){
        return this.f;
    }
    public Float getFObj(){
        return this.fObj;
    }
    public short getS(){
        return this.s;
    }
    public Short getSObj(){
        return this.sObj;
    }
    public Double getDObj(){
        return this.dObj;
    }
    public double getD(){
        return this.d;
    }
    // END
```

## SETTERS

[//]: # (USE SNIPPET ./xetters WITH xetters="setters" xetter="setter" XETTERS="SETTERS" and_not_final=" and not `final`")

The setters segment starts with a line containing `SETTERS` and ends with a line containing
`END`. This segment is overwritten by the handler.

By default pyama will generate setters for those fields that are `private` and not `static` and not `final`.
If the segment starting comment contains the string `for all` then pyama will generate setters
for all the fields.

It is also possible to force individual fields to get setter in the generated code. If the
comment following the field contains `setter` then it will get a setter.

If the comment contains `protected setter` then the setter will have `protected` access modifier.
If the comment contains `package setter` then the setter will have no access modifier and as such
it will be package private.

[//]: # (END SNIPPET)


[//]: # (USE SNIPPET test/MyClass.java/setters)
```java
    // SETTERS
    public void setB(final boolean b){
        this.b = b;
    }
    public void setBObj(final Boolean bObj){
        this.bObj = bObj;
    }
    void setBy(final byte by){
        this.by = by;
    }
    // END
```

## EQUALS

The "equals" segment starts with a line containing `EQUALS` and ends with a line containing
`END`. This segment is overwritten by the handler.

Pyama generates the method `equals()` and `hashCode()`. It is not possible to generate only one.
The calculation of the hash code and the method `equals()` consider only the fields that are
not `static`. There are two strategies that pyama support for the generation of these methods

* `simple` and
* `Objects`

By default the strategy is `Objects`. If the name of the strategy is written following the segment
starting `EQUALS` then that strategy is used. Feel free to play around with the different
strategies and have a look at what code Pyama generates.

You can also use `with getters` and `allow subclass` declarations on the segment starting line.
`with getters` will instruct the code generation to access the fields via the getters. 
`allow_subclass` will instruct the code generation for `equals()` to accept and object, 
which is an instance of a subclass of the current class as a possible equal object.
 

[//]: # (USE SNIPPET test/MyClass.java/equals)
```java
    // EQUALS Objects
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;        

        MyClass other = (MyClass) o;

        if ( b != other.b ) return false;
        if ( by != other.by ) return false;
        if ( !Objects.equals(obj,other.obj) ) return false;
        if ( !Objects.equals(iObj,other.iObj) ) return false;
        if ( i != other.i ) return false;
        if ( l != other.l ) return false;
        if ( !Objects.equals(lObj,other.lObj) ) return false;
        if ( c != other.c ) return false;
        if ( !Objects.equals(cObj,other.cObj) ) return false;
        if (Float.compare(other.f, f) != 0) return false;
        if ( !Objects.equals(fObj,other.fObj) ) return false;
        if ( s != other.s ) return false;
        if ( !Objects.equals(sObj,other.sObj) ) return false;
        if ( !Objects.equals(dObj,other.dObj) ) return false;
        if (Double.compare(other.d, d) != 0) return false;
        return true;
    }
    @Override
    public int hashCode() {
        return Objects.hash(b, by, obj, iObj, i, l, lObj, c, cObj, f, fObj, s, sObj, dObj, d);
    }
    // END
```

## TOSTRING

The "toString" segment starts with a line containing `TOSTRING` and ends with a line containing
`END`. This segment is overwritten by the handler.

Pyama will generate a simple `toString()` method that uses `StringBuilder` and has the format

```bash
classname{field=value,field=value,...,field=value}
```

The only configuration possibility is that you can the handler to use getters. It does that if the `with getters`
is found on the segment starting line.

[//]: # (USE SNIPPET test/MyClass.java/toString)
```java
    // TOSTRING with getters
    @Override
    public String toString() {
        final StringBuilder sb = new StringBuilder("MyClass{");
        sb.append("isB()=").append(isB());
        sb.append(",isBObj()=").append(isBObj());
        sb.append(",getBy()=").append(getBy());
        sb.append(",getObj()=").append(getObj());
        sb.append(",getIObj()=").append(getIObj());
        sb.append(",getI()=").append(getI());
        sb.append(",getL()=").append(getL());
        sb.append(",getLObj()=").append(getLObj());
        sb.append(",getC()=").append(getC());
        sb.append(",getCObj()=").append(getCObj());
        sb.append(",getF()=").append(getF());
        sb.append(",getFObj()=").append(getFObj());
        sb.append(",getS()=").append(getS());
        sb.append(",getSObj()=").append(getSObj());
        sb.append(",getDObj()=").append(getDObj());
        sb.append(",getD()=").append(getD());
        sb.append('}');
        return sb.toString();
    }
    // END
```

## BUILDER

The "builder" segment starts with a line containing `BUILDER` and ends with a line containing
`END`. This segment is overwritten by the handler.

Pyama generates a `public static class` in this segment that is a builder for the surrounding class. If you edit
this line and change the visibility of the class, and the line remains the first line of the segment then
Pyama will respect your change. You can also change the name of the builder class after you generated the
code the first time and Pyama will use the changed name.

Pyama also generates a `public static` method named `builder()` that returns a new instance of the builder
and in the builder class it will generate methods for each field that has to be included in the builder.
A field has to be included in the builder if it is not `static`, not `final` and did not get value assigned
on the line of the declaration. If any of these is true the field will be excluded from the builder. This
algorithm can be overridden with a comment following the field that say `// no builder` to exclude the field
from the builder no matter what or with a comment that says `// builder` to include the field in the builder.
(The `//no builder` is the stronger.)

The builder methods return `this` thus they can be chained. The name of the builder method is `withXxxx` where
`Xxxx` is the name of the field capitalized. You can override this naming specifying a name for the builder method
using the comment on the line of the field declaration that says 
`// builder method "methodname"`. This also forces the field to be included in the 
builder. The name of the method has to be between double quotes.

[//]: # (USE SNIPPET test/MyClass.java/builder)
```java
    // BUILDER
    public static class MyBuilder {
        private MyBuilder(){}
        final MyClass built = new MyClass();
        public MyBuilder build(){
            final MyClass r = built;
            built = null;
            return r;
        }
        public MyBuilder withB(final boolean b){
            built.b = b;
            return this;
        }
        public MyBuilder withBy(final byte by){
            built.by = by;
            return this;
        }
        public MyBuilder withObj(final Object obj){
            built.obj = obj;
            return this;
        }
        public MyBuilder withI(final int i){
            built.i = i;
            return this;
        }
        public MyBuilder withL(final long l){
            built.l = l;
            return this;
        }
        public MyBuilder withLObj(final Long lObj){
            built.lObj = lObj;
            return this;
        }
        public MyBuilder withC(final char c){
            built.c = c;
            return this;
        }
        public MyBuilder separator(final Character cObj){
            built.cObj = cObj;
            return this;
        }
        public MyBuilder withF(final float f){
            built.f = f;
            return this;
        }
        public MyBuilder withFObj(final Float fObj){
            built.fObj = fObj;
            return this;
        }
        public MyBuilder withS(final short s){
            built.s = s;
            return this;
        }
        public MyBuilder withSObj(final Short sObj){
            built.sObj = sObj;
            return this;
        }
        public MyBuilder withDObj(final Double dObj){
            built.dObj = dObj;
            return this;
        }
    public static MyBuilder builder(){
        return new MyBuilder();
    }
    //END
```

The current implementation does not support optional and mandatory builder parameters
and you also can not enforce any ordering.