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

    // FIELDS
    private boolean b;
    static Boolean B;
    byte by;
    Object Obj;
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

    // CONSTRUCTOR
    public MyClass(final double d) {
        this.d = d;
    }
    // END

    // GETTERS for all
    public boolean isB(){
        return this.b;
    }
    public Boolean isB(){
        return this.B;
    }
    public byte getBy(){
        return this.by;
    }
    public Object getObj(){
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

    // SETTERS for all
    public void setB(final boolean b){
        this.b = b;
    }
    public void setB(final Boolean B){
        this.B = B;
    }
    public void setBy(final byte by){
        this.by = by;
    }
    public void setObj(final Object Obj){
        this.Obj = Obj;
    }
    public void setI(final Integer I){
        this.I = I;
    }
    public void setI(final int i){
        this.i = i;
    }
    public void setL(final long l){
        this.l = l;
    }
    public void setL(final Long L){
        this.L = L;
    }
    public void setC(final char c){
        this.c = c;
    }
    public void setC(final Character C){
        this.C = C;
    }
    public void setF(final float f){
        this.f = f;
    }
    public void setF(final Float F){
        this.F = F;
    }
    public void setS(final short s){
        this.s = s;
    }
    public void setS(final Short S){
        this.S = S;
    }
    public void setD(final Double D){
        this.D = D;
    }
    // END

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
}