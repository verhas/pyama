/*
 * Copyright [2018] [Peter Verhas]
 * 
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * 
 *     http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import java.util.Map;

/**
 * This is a Javadoc
 *
 */
public class MyClass {
// START SNIPPET fields
    // FIELDS
    private boolean b; // constructor
    static Boolean bObj; // setter getter
    byte by; //package setter package getter
    Object obj; // package getter
    Integer iObj; // no builder
    int i;
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
        final MyClass built = new MyClass();
        public MyBuilder build(){
            final MyClass r = built;
            built = null;
            return r;
        }
        public MyBuilder withB(final boolean b){
            built.b = b;
            return this;
        }
        public MyBuilder withBy(final byte by){
            built.by = by;
            return this;
        }
        public MyBuilder withObj(final Object obj){
            built.obj = obj;
            return this;
        }
        public MyBuilder withI(final int i){
            built.i = i;
            return this;
        }
        public MyBuilder withL(final long l){
            built.l = l;
            return this;
        }
        public MyBuilder withLObj(final Long lObj){
            built.lObj = lObj;
            return this;
        }
        public MyBuilder withC(final char c){
            built.c = c;
            return this;
        }
        public MyBuilder separator(final Character cObj){
            built.cObj = cObj;
            return this;
        }
        public MyBuilder withF(final float f){
            built.f = f;
            return this;
        }
        public MyBuilder withFObj(final Float fObj){
            built.fObj = fObj;
            return this;
        }
        public MyBuilder withS(final short s){
            built.s = s;
            return this;
        }
        public MyBuilder withSObj(final Short sObj){
            built.sObj = sObj;
            return this;
        }
        public MyBuilder withDObj(final Double dObj){
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
        sb.append("isB()=").append(isB());
        sb.append(",isBObj()=").append(isBObj());
        sb.append(",getBy()=").append(getBy());
        sb.append(",getObj()=").append(getObj());
        sb.append(",getIObj()=").append(getIObj());
        sb.append(",getI()=").append(getI());
        sb.append(",getL()=").append(getL());
        sb.append(",getLObj()=").append(getLObj());
        sb.append(",getC()=").append(getC());
        sb.append(",getCObj()=").append(getCObj());
        sb.append(",getF()=").append(getF());
        sb.append(",getFObj()=").append(getFObj());
        sb.append(",getS()=").append(getS());
        sb.append(",getSObj()=").append(getSObj());
        sb.append(",getDObj()=").append(getDObj());
        sb.append(",getD()=").append(getD());
        sb.append('}');
        return sb.toString();
    }
    // END
//END SNIPPET
}