
/*
 * This is the test LICENSE.txt file
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
    public static class Builder {
        private Builder(){}
        private MyClass built = new MyClass();
        public MyClass build(){
            final MyClass r = built;
            built = null;
            return r;
            }
        public final Builder withB(final boolean b){
        built.b = b;
        return this;
        }
            public final Builder withBy(final byte by){
        built.by = by;
        return this;
        }
            public final Builder withObj(final Object obj){
        built.obj = obj;
        return this;
        }
            public final Builder withIObj(final Integer iObj){
        built.iObj = iObj;
        return this;
        }
            public final Builder withI(final int i){
        built.i = i;
        return this;
        }
            public final Builder withL(final long l){
        built.l = l;
        return this;
        }
            public final Builder withC(final char c){
        built.c = c;
        return this;
        }
            public final Builder separator(final Character cObj){
        built.cObj = cObj;
        return this;
        }
            public final Builder withF(final float f){
        built.f = f;
        return this;
        }
            public final Builder withFObj(final Float fObj){
        built.fObj = fObj;
        return this;
        }
            public final Builder withS(final short s){
        built.s = s;
        return this;
        }
            public final Builder withSObj(final Short sObj){
        built.sObj = sObj;
        return this;
        }
            public final Builder withDObj(final Double dObj){
        built.dObj = dObj;
        return this;
        }
        public static Builder builder(){
            return new Builder();
        }
// END

}