
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

// EQUALS simple with getters
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;

        MyClass other = (MyClass) o;

        if ( isB() != other.isB() ) return false;
        if ( getBy() != other.getBy() ) return false;
        if ( getObj() != null ? !getObj().equals(other.getObj()) : other.getObj() ) ) return false;
        if ( getIObj() != null ? !getIObj().equals(other.getIObj()) : other.getIObj() ) ) return false;
        if ( getI() != other.getI() ) return false;
        if ( getL() != other.getL() ) return false;
        if ( getLObj() != null ? !getLObj().equals(other.getLObj()) : other.getLObj() ) ) return false;
        if ( getC() != other.getC() ) return false;
        if ( getCObj() != null ? !getCObj().equals(other.getCObj()) : other.getCObj() ) ) return false;
        if (Float.compare(other.getF(), getF() ) != 0) return false;
        if ( getFObj() != null ? !getFObj().equals(other.getFObj()) : other.getFObj() ) ) return false;
        if ( getS() != other.getS() ) return false;
        if ( getSObj() != null ? !getSObj().equals(other.getSObj()) : other.getSObj() ) ) return false;
        if ( getDObj() != null ? !getDObj().equals(other.getDObj()) : other.getDObj() ) ) return false;
        if (Double.compare(other.getD(), getD() ) != 0) return false;
        return true;
    }
    @Override
    public int hashCode() {
        int result = 0;
        long temp;

        result = result * 31 + (isB() ? 1 : 0);
        result = result * 31 + (int)getBy();
        result = result * 31 + (getObj() != null ? getObj().hashCode() : 0);
        result = result * 31 + (getIObj() != null ? getIObj().hashCode() : 0);
        result = result * 31 + getI();
        result = result * 31 + (int) (getL() ^ (getL() >>> 32));
        result = result * 31 + (getLObj() != null ? getLObj().hashCode() : 0);
        result = result * 31 + (int)getC();
        result = result * 31 + (getCObj() != null ? getCObj().hashCode() : 0);
        result = result * 31 + (getF() != +0.0f ? Float.floatToIntBits(getF()) : 0);
        result = result * 31 + (getFObj() != null ? getFObj().hashCode() : 0);
        result = result * 31 + (int)getS();
        result = result * 31 + (getSObj() != null ? getSObj().hashCode() : 0);
        result = result * 31 + (getDObj() != null ? getDObj().hashCode() : 0);
        temp = Double.doubleToLongBits(getD());
        result = result * 31 +  (int) (temp ^ (temp >>> 32));

        return result;
    }
// END

}