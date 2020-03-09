
package org.jt.jni.test;

public class BaseExample
{
    public static boolean static_base_boolean_field = false;
    public static char    static_base_char_field    = (char) 1;
    public static byte    static_base_byte_field    = 1;
    public static short   static_base_short_field   = 1;
    public static int     static_base_int_field     = 1;
    public static long    static_base_long_field    = 1;
    public static float   static_base_float_field   = 1.0f;
    public static double  static_base_double_field  = 1.0;
    public static String  static_base_String_field  = "1";

    public boolean base_boolean_field = false;
    public char    base_char_field    = (char) 1;
    public byte    base_byte_field    = 1;
    public short   base_short_field   = 1;
    public int     base_int_field     = 1;
    public long    base_long_field    = 1;
    public float   base_float_field   = 1.0f;
    public double  base_double_field  = 1.0;
    public String  base_String_field  = "1";

    public BaseExample()
    {
        this.base_boolean_field = true;
        this.base_char_field    = (char) 2;
        this.base_byte_field    = 2;
        this.base_short_field   = 2;
        this.base_int_field     = 2;
        this.base_long_field    = 2;
        this.base_float_field   = 2.0f;
        this.base_double_field  = 2.0;
        this.base_String_field  = "2";
    }

    public BaseExample(int value)
    {
        this.base_boolean_field = (value != 0);
        this.base_char_field    = (char) value;
        this.base_byte_field    = (byte) (value % 100);
        this.base_short_field   = (short) value;
        this.base_int_field     = value;
        this.base_long_field    = value;
        this.base_float_field   = value;
        this.base_double_field  = value;
        this.base_String_field  = Integer.toString(value);
    }

    public static boolean get_static_base_boolean_field()
    {
        return BaseExample.static_base_boolean_field;
    }

    public static void set_static_base_boolean_field(boolean value)
    {
        BaseExample.static_base_boolean_field = value;
    }

    public static char get_static_base_char_field()
    {
        return BaseExample.static_base_char_field;
    }

    public static void set_static_base_char_field(char value)
    {
        BaseExample.static_base_char_field = value;
    }

    public static byte get_static_base_byte_field()
    {
        return BaseExample.static_base_byte_field;
    }

    public static void set_static_base_byte_field(byte value)
    {
        BaseExample.static_base_byte_field = value;
    }

    public static short get_static_base_short_field()
    {
        return BaseExample.static_base_short_field;
    }

    public static void set_static_base_short_field(short value)
    {
        BaseExample.static_base_short_field = value;
    }

    public static int get_static_base_int_field()
    {
        return BaseExample.static_base_int_field;
    }

    public static void set_static_base_int_field(int value)
    {
        BaseExample.static_base_int_field = value;
    }

    public static long get_static_base_long_field()
    {
        return BaseExample.static_base_long_field;
    }

    public static void set_static_base_long_field(long value)
    {
        BaseExample.static_base_long_field = value;
    }

    public static float get_static_base_float_field()
    {
        return BaseExample.static_base_float_field;
    }

    public static void set_static_base_float_field(float value)
    {
        BaseExample.static_base_float_field = value;
    }

    public static double get_static_base_double_field()
    {
        return BaseExample.static_base_double_field;
    }

    public static void set_static_base_double_field(double value)
    {
        BaseExample.static_base_double_field = value;
    }

    public static String get_static_base_String_field()
    {
        return BaseExample.static_base_String_field;
    }

    public static void set_static_base_String_field(String value)
    {
        BaseExample.static_base_String_field = value;
    }

    public boolean get_base_boolean_field()
    {
        return this.base_boolean_field;
    }

    public void set_base_boolean_field(boolean value)
    {
        this.base_boolean_field = value;
    }

    public char get_base_char_field()
    {
        return this.base_char_field;
    }

    public void set_base_char_field(char value)
    {
        this.base_char_field = value;
    }

    public byte get_base_byte_field()
    {
        return this.base_byte_field;
    }

    public void set_base_byte_field(byte value)
    {
        this.base_byte_field = value;
    }

    public short get_base_short_field()
    {
        return this.base_short_field;
    }

    public void set_base_short_field(short value)
    {
        this.base_short_field = value;
    }

    public int get_base_int_field()
    {
        return this.base_int_field;
    }

    public void set_base_int_field(int value)
    {
        this.base_int_field = value;
    }

    public long get_base_long_field()
    {
        return this.base_long_field;
    }

    public void set_base_long_field(long value)
    {
        this.base_long_field = value;
    }

    public float get_base_float_field()
    {
        return this.base_float_field;
    }

    public void set_base_float_field(float value)
    {
        this.base_float_field = value;
    }

    public double get_base_double_field()
    {
        return this.base_double_field;
    }

    public void set_base_double_field(double value)
    {
        this.base_double_field = value;
    }

    public String get_base_String_field()
    {
        return this.base_String_field;
    }

    public void set_base_String_field(String value)
    {
        this.base_String_field = value;
    }
}
