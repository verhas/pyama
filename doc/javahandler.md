# Java Handler

The Java Handler can be used to automatically generate

* constructors that will get the arguments for the final fields that are not initialized,
* getters and setters for the fields
* `equals` and `hashCode` (only together, you can not generate only one)
* `toString` method.

The code generation mainly relies on the fields. The fields have to be listed in a snippet 
with the standard Java syntax. There is no need for any extra declaration of the fields and
also fields are part of the hand generated Java code, not overwritten.

[//]: # (USE SNIPPET test/MyClass.java/fields)
```java
    // FIELDS
    private boolean b; // constructor
    static Boolean B; // setter getter
    byte by; //package setter package getter
    Object Obj; // package getter
    Integer I;
    int i;
    long l;
    Long L;
    char c;
    Character C;
    float f;
    Float F;
    short s;
    Short S;
    Double D;
    final double d;
    // END
```

[//]: # (USE SNIPPET test/MyClass.java/constructor)
```java
    // CONSTRUCTOR
    public MyClass(final boolean b, final double d) {
        this.b = b;
        this.d = d;
    }
    // END
```

[//]: # (USE SNIPPET test/MyClass.java/getters)
```java
    // GETTERS for all
    public boolean isB(){
        return this.b;
    }
    public Boolean isB(){
        return this.B;
    }
    byte getBy(){
        return this.by;
    }
    Object getObj(){
        return this.Obj;
    }
    public Integer getI(){
        return this.I;
    }
    public int getI(){
        return this.i;
    }
    public long getL(){
        return this.l;
    }
    public Long getL(){
        return this.L;
    }
    public char getC(){
        return this.c;
    }
    public Character getC(){
        return this.C;
    }
    public float getF(){
        return this.f;
    }
    public Float getF(){
        return this.F;
    }
    public short getS(){
        return this.s;
    }
    public Short getS(){
        return this.S;
    }
    public Double getD(){
        return this.D;
    }
    public double getD(){
        return this.d;
    }
    // END
```

[//]: # (USE SNIPPET test/MyClass.java/setters)
```java
    // SETTERS
    public void setB(final boolean b){
        this.b = b;
    }
    public void setB(final Boolean B){
        this.B = B;
    }
    void setBy(final byte by){
        this.by = by;
    }
    // END
```

[//]: # (USE SNIPPET test/MyClass.java/equals)
```java
    // EQUALS Objects
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;        

        None other = (None) o;

        if ( b != other.b ) return false;
        if ( by != other.by ) return false;
        if ( !Objects.equals(Obj,other.Obj) ) return false;
        if ( !Objects.equals(I,other.I) ) return false;
        if ( i != other.i ) return false;
        if ( l != other.l ) return false;
        if ( !Objects.equals(L,other.L) ) return false;
        if ( c != other.c ) return false;
        if ( !Objects.equals(C,other.C) ) return false;
        if (Float.compare(other.f, f) != 0) return false;
        if ( !Objects.equals(F,other.F) ) return false;
        if ( s != other.s ) return false;
        if ( !Objects.equals(S,other.S) ) return false;
        if ( !Objects.equals(D,other.D) ) return false;
        if (Double.compare(other.d, d) != 0) return false;
        return true;
    }
    @Override
    public int hashCode() {
        return Objects.hash(b, by, Obj, I, i, l, L, c, C, f, F, s, S, D, d);
    }
    // END
```

[//]: # (USE SNIPPET test/MyClass.java/toString)
```java
    // TOSTRING with getters
    @Override
    public String toString() {
        final StringBuilder sb = new StringBuilder("None{");
        sb.append("isB()=").append(isB());
        sb.append("isB()=").append(isB());
        sb.append("getBy()=").append(getBy());
        sb.append("getObj()=").append(getObj());
        sb.append("getI()=").append(getI());
        sb.append("getI()=").append(getI());
        sb.append("getL()=").append(getL());
        sb.append("getL()=").append(getL());
        sb.append("getC()=").append(getC());
        sb.append("getC()=").append(getC());
        sb.append("getF()=").append(getF());
        sb.append("getF()=").append(getF());
        sb.append("getS()=").append(getS());
        sb.append("getS()=").append(getS());
        sb.append("getD()=").append(getD());
        sb.append("getD()=").append(getD());
        sb.append('}');
        return sb.toString();
    }
    // END
```

