
/*
 * This is the test LICENSE.txt file
 */
public class MyClass {
    // FIELDS
    private boolean b; // constructor
    static Boolean bObj; // setter getter
    byte by; //package setter package getter
    Object obj; // package getter
    Integer iObj;
    int i;
    long l;
    Long lObj;
    char c;
    Character cObj;
    float f;
    Float fObj;
    short s;
    Short sObj;
    Double dObj;
    final double d;
    // END

// EQUALS Objects allow subclass
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof MyClass)) return false;

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

}