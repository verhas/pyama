
/**
 * This is a Javadoc
 *
 */
public class MyClass {
    // FIELDS
    private boolean b; // this should get into the constructor
    static Boolean bObj;
    byte by;
    Object obj;
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

// START SNIPPET demo_start_line
    // should remain private and should keep the throws Exception
// CONSTRUCTOR
    private MyClass(final boolean b, final double d) throws Exception {
        super(b,c);
    // START
        this.b = b;
        this.d = d;
        }
// END
// END SNIPPET
}