/*
 * This is the test LICENSE.txt file
 */

import java.util.Map;

/**
 * This is a Javadoc
 *
 */
public class MyClass {
// START SNIPPET fields TEMPLATE MATCH (\w[\w\d_]*)\s*=\s*"(.*?)"
    // MATCH (\w*)="(.*)"
    // VERSION="3.13";
    // NO MATCH
    // FIELDS
    private boolean b; // constructor
    static Boolean bObj; // setter getter
    byte by; //package setter package getter
    Object obj; // package getter
    Integer iObj; // no builder
    int i; // {VERSION}
    long l;
    Long lObj;
    char c;
    Character cObj;  // builder method "separator"
    float f;
    Float fObj;
    short s;
    Short sObj;
    Double dObj;
    final double d;
    // END
// END SNIPPET

// START SNIPPET builder
    // BUILDER
    public static class MyBuilder {
        private MyBuilder(){}
        private MyClass built = new MyClass();
        public MyClass build(){
            final MyClass r = built;
            built = null;
            return r;
            }
        public final MyBuilder withB(final boolean b){
        built.b = b;
        return this;
        }
            public final MyBuilder withBy(final byte by){
        built.by = by;
        return this;
        }
            public final MyBuilder withObj(final Object obj){
        built.obj = obj;
        return this;
        }
            public final MyBuilder withI(final int i){
        built.i = i;
        return this;
        }
            public final MyBuilder withL(final long l){
        built.l = l;
        return this;
        }
            public final MyBuilder withLObj(final Long lObj){
        built.lObj = lObj;
        return this;
        }
            public final MyBuilder withC(final char c){
        built.c = c;
        return this;
        }
            public final MyBuilder separator(final Character cObj){
        built.cObj = cObj;
        return this;
        }
            public final MyBuilder withF(final float f){
        built.f = f;
        return this;
        }
            public final MyBuilder withFObj(final Float fObj){
        built.fObj = fObj;
        return this;
        }
            public final MyBuilder withS(final short s){
        built.s = s;
        return this;
        }
            public final MyBuilder withSObj(final Short sObj){
        built.sObj = sObj;
        return this;
        }
            public final MyBuilder withDObj(final Double dObj){
        built.dObj = dObj;
        return this;
        }
        public static MyBuilder builder(){
            return new MyBuilder();
        }
    //END
// END SNIPPET

// START SNIPPET constructor
    // CONSTRUCTOR
    public MyClass(final boolean b, final double d){
        this.b = b;
        this.d = d;
        }
    // END
//END SNIPPET

// START SNIPPET getters
    // GETTERS for all
    public boolean isB(){
        return this.b;
    }
    public Boolean isBObj(){
        return this.bObj;
    }
    byte getBy(){
        return this.by;
    }
    Object getObj(){
        return this.obj;
    }
    public Integer getIObj(){
        return this.iObj;
    }
    public int getI(){
        return this.i;
    }
    public long getL(){
        return this.l;
    }
    public Long getLObj(){
        return this.lObj;
    }
    public char getC(){
        return this.c;
    }
    public Character getCObj(){
        return this.cObj;
    }
    public float getF(){
        return this.f;
    }
    public Float getFObj(){
        return this.fObj;
    }
    public short getS(){
        return this.s;
    }
    public Short getSObj(){
        return this.sObj;
    }
    public Double getDObj(){
        return this.dObj;
    }
    public double getD(){
        return this.d;
    }
    // END
//END SNIPPET

// START SNIPPET setters
    // SETTERS
    public void setB(final boolean b){
        this.b = b;
    }
    public void setBObj(final Boolean bObj){
        this.bObj = bObj;
    }
    void setBy(final byte by){
        this.by = by;
    }
    // END
//END SNIPPET
// START SNIPPET equals
    // EQUALS Objects
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;

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
//END SNIPPET

// START SNIPPET toString
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
//END SNIPPET
}