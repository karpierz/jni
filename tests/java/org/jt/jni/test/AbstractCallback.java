
package org.jt.jni.test;

public abstract class AbstractCallback implements ICallback
{
    public AbstractCallback()
    {
    }

    public void poke(Example example, boolean value)
    {
        example.set_boolean_field(value);
    }

    public void poke(Example example, char value)
    {
        example.set_char_field((char) (2 * value));
    }

    public void poke(Example example, byte value)
    {
        example.set_byte_field((byte) (2 * value));
    }

    public void poke(Example example, short value)
    {
        example.set_short_field((short) (2 * value));
    }

    public void poke(Example example, int value)
    {
        example.set_int_field(2 * value);
    }

    public void poke(Example example, long value)
    {
        example.set_long_field(2 * value);
    }

    public void poke(Example example, float value)
    {
        example.set_float_field(2 * value);
    }

    public void poke(Example example, double value)
    {
        example.set_double_field(2 * value);
    }

    public void poke(Example example, String value)
    {
        example.set_String_field(value + value);
    }
}
