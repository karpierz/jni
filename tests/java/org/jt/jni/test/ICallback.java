
package org.jt.jni.test;

public interface ICallback
{
    public void poke(Example example, boolean value);
    public void poke(Example example, char    value);
    public void poke(Example example, byte    value);
    public void poke(Example example, short   value);
    public void poke(Example example, int     value);
    public void poke(Example example, long    value);
    public void poke(Example example, float   value);
    public void poke(Example example, double  value);
    public void poke(Example example, String  value);

    public void peek(Example example, int value);
}
