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
public class MyClass implements ScriptBasic {
// START SNIPPET fields
    // FIELDS
    private boolean b; // constructor
    static Boolean B; // setter getter
    byte by; //package setter package getter
    Object Obj; // package getter
    Integer I;
    int i;
    long l;
    Long L;
    char c;
    Character C;
    float f;
    Float F;
    short s;
    Short S;
    Double D;
    final double d;
    // END
// END SNIPPET

// START SNIPPET constructor
    // CONSTRUCTOR
    public MyClass(final boolean b, final double d) {
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
    public Boolean isB(){
        return this.B;
    }
    byte getBy(){
        return this.by;
    }
    Object getObj(){
        return this.Obj;
    }
    public Integer getI(){
        return this.I;
    }
    public int getI(){
        return this.i;
    }
    public long getL(){
        return this.l;
    }
    public Long getL(){
        return this.L;
    }
    public char getC(){
        return this.c;
    }
    public Character getC(){
        return this.C;
    }
    public float getF(){
        return this.f;
    }
    public Float getF(){
        return this.F;
    }
    public short getS(){
        return this.s;
    }
    public Short getS(){
        return this.S;
    }
    public Double getD(){
        return this.D;
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
    public void setB(final Boolean B){
        this.B = B;
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

        None other = (None) o;

        if ( b != other.b ) return false;
        if ( by != other.by ) return false;
        if ( !Objects.equals(Obj,other.Obj) ) return false;
        if ( !Objects.equals(I,other.I) ) return false;
        if ( i != other.i ) return false;
        if ( l != other.l ) return false;
        if ( !Objects.equals(L,other.L) ) return false;
        if ( c != other.c ) return false;
        if ( !Objects.equals(C,other.C) ) return false;
        if (Float.compare(other.f, f) != 0) return false;
        if ( !Objects.equals(F,other.F) ) return false;
        if ( s != other.s ) return false;
        if ( !Objects.equals(S,other.S) ) return false;
        if ( !Objects.equals(D,other.D) ) return false;
        if (Double.compare(other.d, d) != 0) return false;
        return true;
    }
    @Override
    public int hashCode() {
        return Objects.hash(b, by, Obj, I, i, l, L, c, C, f, F, s, S, D, d);
    }
    // END
//END SNIPPET

// START SNIPPET toString
    // TOSTRING with getters
    @Override
    public String toString() {
        final StringBuilder sb = new StringBuilder("None{");
        sb.append("isB()=").append(isB());
        sb.append("isB()=").append(isB());
        sb.append("getBy()=").append(getBy());
        sb.append("getObj()=").append(getObj());
        sb.append("getI()=").append(getI());
        sb.append("getI()=").append(getI());
        sb.append("getL()=").append(getL());
        sb.append("getL()=").append(getL());
        sb.append("getC()=").append(getC());
        sb.append("getC()=").append(getC());
        sb.append("getF()=").append(getF());
        sb.append("getF()=").append(getF());
        sb.append("getS()=").append(getS());
        sb.append("getS()=").append(getS());
        sb.append("getD()=").append(getD());
        sb.append("getD()=").append(getD());
        sb.append('}');
        return sb.toString();
    }
    // END
//END SNIPPET
}