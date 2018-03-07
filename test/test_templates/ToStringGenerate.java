
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

// TOSTRING
            @Override
            public String toString() {
                final StringBuilder sb = new StringBuilder("MyClass{");
                sb.append("b=").append(b);
                sb.append(",")
                sb.append("bObj=").append(bObj);
                sb.append(",")
                sb.append("by=").append(by);
                sb.append(",")
                sb.append("obj=").append(obj);
                sb.append(",")
                sb.append("iObj=").append(iObj);
                sb.append(",")
                sb.append("i=").append(i);
                sb.append(",")
                sb.append("l=").append(l);
                sb.append(",")
                sb.append("lObj=").append(lObj);
                sb.append(",")
                sb.append("c=").append(c);
                sb.append(",")
                sb.append("cObj=").append(cObj);
                sb.append(",")
                sb.append("f=").append(f);
                sb.append(",")
                sb.append("fObj=").append(fObj);
                sb.append(",")
                sb.append("s=").append(s);
                sb.append(",")
                sb.append("sObj=").append(sObj);
                sb.append(",")
                sb.append("dObj=").append(dObj);
                sb.append(",")
                sb.append("d=").append(d);
                sb.append("}");
                return sb.toString();
            }
// END

}