
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

// TOSTRING with getters
            @Override
            public String toString() {
                final StringBuilder sb = new StringBuilder("MyClass{");
                sb.append("b=").append(isB());
                sb.append(",")
                sb.append("bObj=").append(isBObj());
                sb.append(",")
                sb.append("by=").append(getBy());
                sb.append(",")
                sb.append("obj=").append(getObj());
                sb.append(",")
                sb.append("iObj=").append(getIObj());
                sb.append(",")
                sb.append("i=").append(getI());
                sb.append(",")
                sb.append("l=").append(getL());
                sb.append(",")
                sb.append("lObj=").append(getLObj());
                sb.append(",")
                sb.append("c=").append(getC());
                sb.append(",")
                sb.append("cObj=").append(getCObj());
                sb.append(",")
                sb.append("f=").append(getF());
                sb.append(",")
                sb.append("fObj=").append(getFObj());
                sb.append(",")
                sb.append("s=").append(getS());
                sb.append(",")
                sb.append("sObj=").append(getSObj());
                sb.append(",")
                sb.append("dObj=").append(getDObj());
                sb.append(",")
                sb.append("d=").append(getD());
                sb.append("}");
                return sb.toString();
            }
// END

}