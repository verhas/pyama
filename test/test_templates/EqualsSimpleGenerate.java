
/**
 * This is a Javadoc
 *
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

// EQUALS simple
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;

        MyClass other = (MyClass) o;

        if ( b != other.b ) return false;
        if ( by != other.by ) return false;
        if ( obj != null ? !obj.equals(other.obj) : other.obj != null ) return false;
        if ( iObj != null ? !iObj.equals(other.iObj) : other.iObj != null ) return false;
        if ( i != other.i ) return false;
        if ( l != other.l ) return false;
        if ( lObj != null ? !lObj.equals(other.lObj) : other.lObj != null ) return false;
        if ( c != other.c ) return false;
        if ( cObj != null ? !cObj.equals(other.cObj) : other.cObj != null ) return false;
        if (Float.compare(other.f, f) != 0) return false;
        if ( fObj != null ? !fObj.equals(other.fObj) : other.fObj != null ) return false;
        if ( s != other.s ) return false;
        if ( sObj != null ? !sObj.equals(other.sObj) : other.sObj != null ) return false;
        if ( dObj != null ? !dObj.equals(other.dObj) : other.dObj != null ) return false;
        if (Double.compare(other.d, d) != 0) return false;
        return true;
    }
    @Override
    public int hashCode() {
        int result = 0;
        long temp;

        result = result * 31 + (b ? 1 : 0);
        result = result * 31 + (int)by;
        result = result * 31 + (obj != null ? obj.hashCode() : 0);
        result = result * 31 + (iObj != null ? iObj.hashCode() : 0);
        result = result * 31 + i;
        result = result * 31 + (int) (l ^ (l >>> 32));
        result = result * 31 + (lObj != null ? lObj.hashCode() : 0);
        result = result * 31 + (int)c;
        result = result * 31 + (cObj != null ? cObj.hashCode() : 0);
        result = result * 31 + (f != +0.0f ? Float.floatToIntBits(f) : 0);
        result = result * 31 + (fObj != null ? fObj.hashCode() : 0);
        result = result * 31 + (int)s;
        result = result * 31 + (sObj != null ? sObj.hashCode() : 0);
        result = result * 31 + (dObj != null ? dObj.hashCode() : 0);
        temp = Double.doubleToLongBits(d);
        result = result * 31 +  (int) (temp ^ (temp >>> 32));
        return result;
    }
// END

}