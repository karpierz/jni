
package org.jt.jni.test;

import java.lang.Math;

public class Example extends BaseExample
{
    /* Static fields and methods */

    public static boolean static_boolean_field = false;
    public static char    static_char_field    = (char) 11;
    public static byte    static_byte_field    = 11;
    public static short   static_short_field   = 11;
    public static int     static_int_field     = 11;
    public static long    static_long_field    = 11;
    public static float   static_float_field   = 11.0f;
    public static double  static_double_field  = 11.0;
    public static String  static_String_field  = "11";

    public boolean boolean_field = false;
    public char    char_field    = (char) 33;
    public byte    byte_field    = 33;
    public short   short_field   = 33;
    public int     int_field     = 33;
    public long    long_field    = 33;
    public float   float_field   = 33.0f;
    public double  double_field  = 33.0;
    public String  String_field  = "33";

    /* An inner enumerated type */
    public enum Stuff
    {
        FOO, BAR, WHIZ;
    }

    /* Public member fields and method */
    public Thing theThing;

    /* Polymorphic constructors */

    public Example()
    {
        super(22);
        this.boolean_field = false;
        this.char_field    = (char) 33;
        this.byte_field    = 33;
        this.short_field   = 33;
        this.int_field     = 33;
        this.long_field    = 33;
        this.float_field   = 33.0f;
        this.double_field  = 33.0;
        this.String_field  = "33";
    }

    public Example(int value)
    {
        super(44);
        this.boolean_field = (value != 0);
        this.char_field    = (char) value;
        this.byte_field    = (byte) (value % 100);
        this.short_field   = (short) value;
        this.int_field     = value;
        this.long_field    = value;
        this.float_field   = value;
        this.double_field  = value;
        this.String_field  = Integer.toString(value);
    }

    public Example(int base_value, int value)
    {
        super(base_value);
        this.boolean_field = (value != 0);
        this.char_field    = (char) value;
        this.byte_field    = (byte) (value % 100);
        this.short_field   = (short) value;
        this.int_field     = value;
        this.long_field    = value;
        this.float_field   = value;
        this.double_field  = value;
        this.String_field  = Integer.toString(value);
    }

    protected Example(String value)
    {
        // A protected constructor - it exists, but can't be accessed by Python.
        super(999);
    }

    /* Accessor/mutator methods */

    public static boolean get_static_boolean_field()
    {
        return Example.static_boolean_field;
    }

    public static void set_static_boolean_field(boolean value)
    {
        Example.static_boolean_field = value;
    }

    public static char get_static_char_field()
    {
        return Example.static_char_field;
    }

    public static void set_static_char_field(char value)
    {
        Example.static_char_field = value;
    }

    public static byte get_static_byte_field()
    {
        return Example.static_byte_field;
    }

    public static void set_static_byte_field(byte value)
    {
        Example.static_byte_field = value;
    }

    public static short get_static_short_field()
    {
        return Example.static_short_field;
    }

    public static void set_static_short_field(short value)
    {
        Example.static_short_field = value;
    }

    public static int get_static_int_field()
    {
        return Example.static_int_field;
    }

    public static void set_static_int_field(int value)
    {
        Example.static_int_field = value;
    }

    public static long get_static_long_field()
    {
        return Example.static_long_field;
    }

    public static void set_static_long_field(long value)
    {
        Example.static_long_field = value;
    }

    public static float get_static_float_field()
    {
        return Example.static_float_field;
    }

    public static void set_static_float_field(float value)
    {
        Example.static_float_field = value;
    }

    public static double get_static_double_field()
    {
        return Example.static_double_field;
    }

    public static void set_static_double_field(double value)
    {
        Example.static_double_field = value;
    }

    public static String get_static_String_field()
    {
        return Example.static_String_field;
    }

    public static void set_static_String_field(String value)
    {
        Example.static_String_field = value;
    }

    public boolean get_boolean_field()
    {
        return this.boolean_field;
    }

    public void set_boolean_field(boolean value)
    {
        this.boolean_field = value;
    }

    public char get_char_field()
    {
        return this.char_field;
    }

    public void set_char_field(char value)
    {
        this.char_field = value;
    }

    public byte get_byte_field()
    {
        return this.byte_field;
    }

    public void set_byte_field(byte value)
    {
        this.byte_field = value;
    }

    public short get_short_field()
    {
        return this.short_field;
    }

    public void set_short_field(short value)
    {
        this.short_field = value;
    }

    public int get_int_field()
    {
        return this.int_field;
    }

    public void set_int_field(int value)
    {
        this.int_field = value;
    }

    public long get_long_field()
    {
        return this.long_field;
    }

    public void set_long_field(long value)
    {
        this.long_field = value;
    }

    public float get_float_field()
    {
        return this.float_field;
    }

    public void set_float_field(float value)
    {
        this.float_field = value;
    }

    public double get_double_field()
    {
        return this.double_field;
    }

    public void set_double_field(double value)
    {
        this.double_field = value;
    }

    public String get_String_field()
    {
        return this.String_field;
    }

    public void set_String_field(String value)
    {
        this.String_field = value;
    }

    /* Polymorphism handling */

    public byte doubler(boolean in)
    {
        return (byte) (in ? 2 : 0);
    }

    public char doubler(char in)
    {
        return (char) (in + in);
    }

    public byte doubler(byte in)
    {
        return (byte) (in + in);
    }

    public short doubler(short in)
    {
        return (byte) (in + in);
    }

    public int doubler(int in)
    {
        return in + in;
    }

    public long doubler(long in)
    {
        return in + in;
    }

    public float doubler(float in)
    {
        return in + in;
    }

    public double doubler(double in)
    {
        return in + in;
    }

    public String doubler(String in)
    {
        return in + in;
    }

    public static byte tripler(boolean in)
    {
        return (byte) (in ? 3 : 0);
    }

    public static char tripler(char in)
    {
        return (char) (in + in + in);
    }

    public static byte tripler(byte in)
    {
        return (byte) (in + in + in);
    }

    public static short tripler(short in)
    {
        return (byte) (in + in + in);
    }

    public static int tripler(int in)
    {
        return in + in + in;
    }

    public static long tripler(long in)
    {
        return in + in + in;
    }

    public static float tripler(float in)
    {
        return in + in + in;
    }

    public static double tripler(double in)
    {
        return in + in + in;
    }

    public static String tripler(String in)
    {
        return in + in + in;
    }

    /* Float/Double argument/return value handling */

    public float area_of_square(float size)
    {
        return size * size;
    }

    public double area_of_circle(double diameter)
    {
        return 0.25 * (Math.PI * (diameter * diameter));
    }

    /* Enum argument handling */

    public String label(Stuff value)
    {
        switch ( value )
        {
            case FOO:  return "Foo";
            case BAR:  return "Bar";
            case WHIZ: return "Whiz";
            default:   return "Unknown";
        }
    }

    /* Handling of object references. */
    public void set_thing(Thing thing)
    {
        this.theThing = thing;
    }

    public Thing get_thing()
    {
        return this.theThing;
    }

    /* String argument/return value handling */
    public String duplicate_string(String in)
    {
        return in + in;
    }

    /* Interface visiblity */

    protected static int  static_invisible_field;
    protected        int  invisible_field;

    protected static void static_invisible_method(int value) { }
    protected        void invisible_method(int value) { }

    /* Callback handling */

    private ICallback callback;

    public void set_callback(ICallback cb)
    {
        this.callback = cb;
    }

    public void test_peek(int value)
    {
        this.callback.peek(this, value);
    }

    public void test_poke(int value)
    {
        this.callback.poke(this, value);
    }

    /* General utility - converting objects to string */

    public String toString()
    {
        return "This is a Java Example object";
    }

    /* Inner classes */

    public class Inner
    {
        public static final int INNER_CONSTANT = 1234;

        public Inner()
        {
        }

        int the_answer(boolean correct)
        {
            if ( correct )
                return 42;
            else
                return 54;
        }
    }
}
