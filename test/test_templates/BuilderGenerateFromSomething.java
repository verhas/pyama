
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
    Long lObj; // no builder
    char c;
    Character cObj; // builder method "separator"
    float f;
    Float fObj;
    short s;
    Short sObj;
    Double dObj;
    final double d;
    // END

// BUILDER
     static class MySpeciallyNamedBuilder {
        private MySpeciallyNamedBuilder(){}
        private MyClass built = new MyClass();
        public MyClass build(){
            final MyClass r = built;
            built = null;
            return r;
            }
            public final MySpeciallyNamedBuilder withB(final boolean b){
            built.b = b;
            return this;
            }
                public final MySpeciallyNamedBuilder withBy(final byte by){
            built.by = by;
            return this;
            }
                public final MySpeciallyNamedBuilder withObj(final Object obj){
            built.obj = obj;
            return this;
            }
                public final MySpeciallyNamedBuilder withIObj(final Integer iObj){
            built.iObj = iObj;
            return this;
            }
                public final MySpeciallyNamedBuilder withI(final int i){
            built.i = i;
            return this;
            }
                public final MySpeciallyNamedBuilder withL(final long l){
            built.l = l;
            return this;
            }
                public final MySpeciallyNamedBuilder withC(final char c){
            built.c = c;
            return this;
            }
                public final MySpeciallyNamedBuilder separator(final Character cObj){
            built.cObj = cObj;
            return this;
            }
                public final MySpeciallyNamedBuilder withF(final float f){
            built.f = f;
            return this;
            }
                public final MySpeciallyNamedBuilder withFObj(final Float fObj){
            built.fObj = fObj;
            return this;
            }
                public final MySpeciallyNamedBuilder withS(final short s){
            built.s = s;
            return this;
            }
                public final MySpeciallyNamedBuilder withSObj(final Short sObj){
            built.sObj = sObj;
            return this;
            }
                public final MySpeciallyNamedBuilder withDObj(final Double dObj){
            built.dObj = dObj;
            return this;
            }
        public static MySpeciallyNamedBuilder builder(){
            return new MySpeciallyNamedBuilder();
        }
// END

}