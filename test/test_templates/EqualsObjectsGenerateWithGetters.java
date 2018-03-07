
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

// EQUALS Objects with getters
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;

        MyClass other = (MyClass) o;

        if ( isB() != other.isB() ) return false;
        if ( getBy() != other.getBy() ) return false;
        if ( !Objects.equals(getObj(),other.getObj() ) ) return false;
        if ( !Objects.equals(getIObj(),other.getIObj() ) ) return false;
        if ( getI() != other.getI() ) return false;
        if ( getL() != other.getL() ) return false;
        if ( !Objects.equals(getLObj(),other.getLObj() ) ) return false;
        if ( getC() != other.getC() ) return false;
        if ( !Objects.equals(getCObj(),other.getCObj() ) ) return false;
        if (Float.compare(other.getF(), getF() ) != 0) return false;
        if ( !Objects.equals(getFObj(),other.getFObj() ) ) return false;
        if ( getS() != other.getS() ) return false;
        if ( !Objects.equals(getSObj(),other.getSObj() ) ) return false;
        if ( !Objects.equals(getDObj(),other.getDObj() ) ) return false;
        if (Double.compare(other.getD(), getD() ) != 0) return false;
        return true;
    }
    @Override
    public int hashCode() {
        return Objects.hash(isB(), getBy(), getObj(), getIObj(), getI(), getL(), getLObj(), getC(), getCObj(), getF(), getFObj(), getS(), getSObj(), getDObj(), getD());
    }
// END

}