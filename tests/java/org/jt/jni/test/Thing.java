
package org.jt.jni.test;

public class Thing
{
    public static int static_int_field = 11;

    public static String name;

    public Thing(String n)
    {
        name = n;
    }

    public Thing(String n, int count)
    {
        name = n + " " + count;
    }

    public String toString()
    {
        return name;
    }
}
