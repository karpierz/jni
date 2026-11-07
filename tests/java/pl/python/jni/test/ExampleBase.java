// Copyright (c) 2004 Adam Karpierz
// SPDX-License-Identifier: CC-BY-NC-ND-4.0 OR LicenseRef-Proprietary
// Please refer to the accompanying LICENSE file.

package pl.python.jni.test;

public class ExampleBase
{
    // Static fields
    public static boolean static_base_boolean_field = false;
    public static char    static_base_char_field    = (char) 1;
    public static byte    static_base_byte_field    = (byte) 1;
    public static short   static_base_short_field   = (short) 1;
    public static int     static_base_int_field     = 1;
    public static long    static_base_long_field    = 1L;
    public static float   static_base_float_field   = 1.0f;
    public static double  static_base_double_field  = 1.0;
    public static String  static_base_String_field  = "1";

    // Static array fields
    public static boolean[] static_base_boolean_array_field = {false, true};
    public static char[]    static_base_char_array_field    = {(char) 1, (char) 2};
    public static byte[]    static_base_byte_array_field    = {(byte) 1, (byte) 2};
    public static short[]   static_base_short_array_field   = {(short) 1, (short) 2};
    public static int[]     static_base_int_array_field     = {1, 2};
    public static long[]    static_base_long_array_field    = {1L, 2L};
    public static float[]   static_base_float_array_field   = {1.0f, 2.5f};
    public static double[]  static_base_double_array_field  = {1.0, 2.5};
    public static String[]  static_base_String_array_field  = {"1", "2"};

    // Static 2D array fields
    public static boolean[][] static_base_boolean_array2D_field = {{false, true},
                                                                   {true, false}};
    public static char[][]    static_base_char_array2D_field    = {{(char) 1, (char) 2},
                                                                   {(char) 3, (char) 4}};
    public static byte[][]    static_base_byte_array2D_field    = {{(byte) 1, (byte) 2},
                                                                   {(byte) 3, (byte) 4}};
    public static short[][]   static_base_short_array2D_field   = {{(short) 1, (short) 2},
                                                                   {(short) 3, (short) 4}};
    public static int[][]     static_base_int_array2D_field     = {{1, 2},
                                                                   {3, 4}};
    public static long[][]    static_base_long_array2D_field    = {{1L, 2L},
                                                                   {3L, 4L}};
    public static float[][]   static_base_float_array2D_field   = {{1.0f, 2.5f},
                                                                   {3.0f, 4.5f}};
    public static double[][]  static_base_double_array2D_field  = {{1.0, 2.5},
                                                                   {3.0, 4.5}};
    public static String[][]  static_base_String_array2D_field  = {{"1", "2"},
                                                                   {"3", "4"}};

    // Instance fields
    public boolean base_boolean_field = false;
    public char    base_char_field    = (char) 1;
    public byte    base_byte_field    = (byte) 1;
    public short   base_short_field   = (short) 1;
    public int     base_int_field     = 1;
    public long    base_long_field    = 1L;
    public float   base_float_field   = 1.0f;
    public double  base_double_field  = 1.0;
    public String  base_String_field  = "1";

    // Instance array fields
    public boolean[] base_boolean_array_field = {false, true};
    public char[]    base_char_array_field    = {(char) 1, (char) 2};
    public byte[]    base_byte_array_field    = {(byte) 1, (byte) 2};
    public short[]   base_short_array_field   = {(short) 1, (short) 2};
    public int[]     base_int_array_field     = {1, 2};
    public long[]    base_long_array_field    = {1L, 2L};
    public float[]   base_float_array_field   = {1.0f, 2.5f};
    public double[]  base_double_array_field  = {1.0, 2.5};
    public String[]  base_String_array_field  = {"1", "2"};

    // Instance 2D array fields
    public boolean[][] base_boolean_array2D_field = {{false, true},
                                                     {true, false}};
    public char[][]    base_char_array2D_field    = {{(char) 1, (char) 2},
                                                     {(char) 3, (char) 4}};
    public byte[][]    base_byte_array2D_field    = {{(byte) 1, (byte) 2},
                                                     {(byte) 3, (byte) 4}};
    public short[][]   base_short_array2D_field   = {{(short) 1, (short) 2},
                                                     {(short) 3, (short) 4}};
    public int[][]     base_int_array2D_field     = {{1, 2},
                                                     {3, 4}};
    public long[][]    base_long_array2D_field    = {{1L, 2L},
                                                     {3L, 4L}};
    public float[][]   base_float_array2D_field   = {{1.0f, 2.5f},
                                                     {3.0f, 4.5f}};
    public double[][]  base_double_array2D_field  = {{1.0, 2.5},
                                                     {3.0, 4.5}};
    public String[][]  base_String_array2D_field  = {{"1", "2"},
                                                     {"3", "4"}};

    public ExampleBase()
    {
        this.init_instance_fields(2);
    }

    public ExampleBase(int value)
    {
        this.init_instance_fields(value);
    }

    private void init_instance_fields(int value)
    {
        this.base_boolean_field = (value != 0);
        this.base_char_field    = (char) value;
        this.base_byte_field    = (byte) (value % 100);
        this.base_short_field   = (short) value;
        this.base_int_field     = value;
        this.base_long_field    = (long) value;
        this.base_float_field   = (float) value;
        this.base_double_field  = (double) value;
        this.base_String_field  = Integer.toString(value);

        this.base_boolean_array_field = new boolean[] {(value != 0), (value == 0)};
        this.base_char_array_field    = new char[]    {(char) value, (char) (value + 1)};
        this.base_byte_array_field    = new byte[]    {(byte) (value % 100), (byte) (value % 50)};
        this.base_short_array_field   = new short[]   {(short) value, (short) (value + 1)};
        this.base_int_array_field     = new int[]     {value, value + 1};
        this.base_long_array_field    = new long[]    {(long) value, (long) value + 1L};
        this.base_float_array_field   = new float[]   {(float) (value + 0.5), (float) (value + 1.0)};
        this.base_double_array_field  = new double[]  {(double) value + 0.5, (double) value + 1.0};
        this.base_String_array_field  = new String[]  {Integer.toString(value), Integer.toString(value + 1)};

        this.base_boolean_array2D_field = new boolean[][] {{(value != 0), (value == 0)},
                                                           {(value == 0), (value != 0)}};
        this.base_char_array2D_field    = new char[][]    {{(char) value, (char) (value + 1)},
                                                           {(char) (value + 2), (char) (value + 3)}};
        this.base_byte_array2D_field    = new byte[][]    {{(byte) (value % 100), (byte) (value % 50)},
                                                           {(byte) (value % 25), (byte) (value % 10)}};
        this.base_short_array2D_field   = new short[][]   {{(short) value, (short) (value + 1)},
                                                           {(short) (value + 2), (short) (value + 3)}};
        this.base_int_array2D_field     = new int[][]     {{value, value + 1},
                                                           {value + 2, value + 3}};
        this.base_long_array2D_field    = new long[][]    {{(long) value, (long) value + 1L},
                                                           {(long) value + 2L, (long) value + 3L}};
        this.base_float_array2D_field   = new float[][]   {{(float) value, (float) (value + 1.0 + 0.5)},
                                                           {(float) (value + 2.0), (float) (value + 3.0 + 0.5)}};
        this.base_double_array2D_field  = new double[][]  {{(double) value, (double) value + 1.0 + 0.5},
                                                           {(double) value + 2.0, (double) value + 3.0 + 0.5}};
        this.base_String_array2D_field  = new String[][]  {{Integer.toString(value), Integer.toString(value + 1)},
                                                           {Integer.toString(value + 2), Integer.toString(value + 3)}};
    }

    // Accessor/mutator methods

    // Static methods

    public static boolean get_static_base_boolean_field()
    {
        return ExampleBase.static_base_boolean_field;
    }

    public static void set_static_base_boolean_field(boolean value)
    {
        ExampleBase.static_base_boolean_field = value;
    }

    public static char get_static_base_char_field()
    {
        return ExampleBase.static_base_char_field;
    }

    public static void set_static_base_char_field(char value)
    {
        ExampleBase.static_base_char_field = value;
    }

    public static byte get_static_base_byte_field()
    {
        return ExampleBase.static_base_byte_field;
    }

    public static void set_static_base_byte_field(byte value)
    {
        ExampleBase.static_base_byte_field = value;
    }

    public static short get_static_base_short_field()
    {
        return ExampleBase.static_base_short_field;
    }

    public static void set_static_base_short_field(short value)
    {
        ExampleBase.static_base_short_field = value;
    }

    public static int get_static_base_int_field()
    {
        return ExampleBase.static_base_int_field;
    }

    public static void set_static_base_int_field(int value)
    {
        ExampleBase.static_base_int_field = value;
    }

    public static long get_static_base_long_field()
    {
        return ExampleBase.static_base_long_field;
    }

    public static void set_static_base_long_field(long value)
    {
        ExampleBase.static_base_long_field = value;
    }

    public static float get_static_base_float_field()
    {
        return ExampleBase.static_base_float_field;
    }

    public static void set_static_base_float_field(float value)
    {
        ExampleBase.static_base_float_field = value;
    }

    public static double get_static_base_double_field()
    {
        return ExampleBase.static_base_double_field;
    }

    public static void set_static_base_double_field(double value)
    {
        ExampleBase.static_base_double_field = value;
    }

    public static String get_static_base_String_field()
    {
        return ExampleBase.static_base_String_field;
    }

    public static void set_static_base_String_field(String value)
    {
        ExampleBase.static_base_String_field = value;
    }

    // Static array methods

    public static boolean[] get_static_base_boolean_array_field()
    {
        return ExampleBase.static_base_boolean_array_field;
    }

    public static void set_static_base_boolean_array_field(boolean[] value)
    {
        ExampleBase.static_base_boolean_array_field = value;
    }

    public static char[] get_static_base_char_array_field()
    {
        return ExampleBase.static_base_char_array_field;
    }

    public static void set_static_base_char_array_field(char[] value)
    {
        ExampleBase.static_base_char_array_field = value;
    }

    public static byte[] get_static_base_byte_array_field()
    {
        return ExampleBase.static_base_byte_array_field;
    }

    public static void set_static_base_byte_array_field(byte[] value)
    {
        ExampleBase.static_base_byte_array_field = value;
    }

    public static short[] get_static_base_short_array_field()
    {
        return ExampleBase.static_base_short_array_field;
    }

    public static void set_static_base_short_array_field(short[] value)
    {
        ExampleBase.static_base_short_array_field = value;
    }

    public static int[] get_static_base_int_array_field()
    {
        return ExampleBase.static_base_int_array_field;
    }

    public static void set_static_base_int_array_field(int[] value)
    {
        ExampleBase.static_base_int_array_field = value;
    }

    public static long[] get_static_base_long_array_field()
    {
        return ExampleBase.static_base_long_array_field;
    }

    public static void set_static_base_long_array_field(long[] value)
    {
        ExampleBase.static_base_long_array_field = value;
    }

    public static float[] get_static_base_float_array_field()
    {
        return ExampleBase.static_base_float_array_field;
    }

    public static void set_static_base_float_array_field(float[] value)
    {
        ExampleBase.static_base_float_array_field = value;
    }

    public static double[] get_static_base_double_array_field()
    {
        return ExampleBase.static_base_double_array_field;
    }

    public static void set_static_base_double_array_field(double[] value)
    {
        ExampleBase.static_base_double_array_field = value;
    }

    public static String[] get_static_base_String_array_field()
    {
        return ExampleBase.static_base_String_array_field;
    }

    public static void set_static_base_String_array_field(String[] value)
    {
        ExampleBase.static_base_String_array_field = value;
    }

    // Static 2D array methods

    public static boolean[][] get_static_base_boolean_array2D_field()
    {
        return ExampleBase.static_base_boolean_array2D_field;
    }

    public static void set_static_base_boolean_array2D_field(boolean[][] value)
    {
        ExampleBase.static_base_boolean_array2D_field = value;
    }

    public static char[][] get_static_base_char_array2D_field()
    {
        return ExampleBase.static_base_char_array2D_field;
    }

    public static void set_static_base_char_array2D_field(char[][] value)
    {
        ExampleBase.static_base_char_array2D_field = value;
    }

    public static byte[][] get_static_base_byte_array2D_field()
    {
        return ExampleBase.static_base_byte_array2D_field;
    }

    public static void set_static_base_byte_array2D_field(byte[][] value)
    {
        ExampleBase.static_base_byte_array2D_field = value;
    }

    public static short[][] get_static_base_short_array2D_field()
    {
        return ExampleBase.static_base_short_array2D_field;
    }

    public static void set_static_base_short_array2D_field(short[][] value)
    {
        ExampleBase.static_base_short_array2D_field = value;
    }

    public static int[][] get_static_base_int_array2D_field()
    {
        return ExampleBase.static_base_int_array2D_field;
    }

    public static void set_static_base_int_array2D_field(int[][] value)
    {
        ExampleBase.static_base_int_array2D_field = value;
    }

    public static long[][] get_static_base_long_array2D_field()
    {
        return ExampleBase.static_base_long_array2D_field;
    }

    public static void set_static_base_long_array2D_field(long[][] value)
    {
        ExampleBase.static_base_long_array2D_field = value;
    }

    public static float[][] get_static_base_float_array2D_field()
    {
        return ExampleBase.static_base_float_array2D_field;
    }

    public static void set_static_base_float_array2D_field(float[][] value)
    {
        ExampleBase.static_base_float_array2D_field = value;
    }

    public static double[][] get_static_base_double_array2D_field()
    {
        return ExampleBase.static_base_double_array2D_field;
    }

    public static void set_static_base_double_array2D_field(double[][] value)
    {
        ExampleBase.static_base_double_array2D_field = value;
    }

    public static String[][] get_static_base_String_array2D_field()
    {
        return ExampleBase.static_base_String_array2D_field;
    }

    public static void set_static_base_String_array2D_field(String[][] value)
    {
        ExampleBase.static_base_String_array2D_field = value;
    }

    // Instance methods

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

    // Instance array methods

    public boolean[] get_base_boolean_array_field()
    {
        return this.base_boolean_array_field;
    }

    public void set_base_boolean_array_field(boolean[] value)
    {
        this.base_boolean_array_field = value;
    }

    public char[] get_base_char_array_field()
    {
        return this.base_char_array_field;
    }

    public void set_base_char_array_field(char[] value)
    {
        this.base_char_array_field = value;
    }

    public byte[] get_base_byte_array_field()
    {
        return this.base_byte_array_field;
    }

    public void set_base_byte_array_field(byte[] value)
    {
        this.base_byte_array_field = value;
    }

    public short[] get_base_short_array_field()
    {
        return this.base_short_array_field;
    }

    public void set_base_short_array_field(short[] value)
    {
        this.base_short_array_field = value;
    }

    public int[] get_base_int_array_field()
    {
        return this.base_int_array_field;
    }

    public void set_base_int_array_field(int[] value)
    {
        this.base_int_array_field = value;
    }

    public long[] get_base_long_array_field()
    {
        return this.base_long_array_field;
    }

    public void set_base_long_array_field(long[] value)
    {
        this.base_long_array_field = value;
    }

    public float[] get_base_float_array_field()
    {
        return this.base_float_array_field;
    }

    public void set_base_float_array_field(float[] value)
    {
        this.base_float_array_field = value;
    }

    public double[] get_base_double_array_field()
    {
        return this.base_double_array_field;
    }

    public void set_base_double_array_field(double[] value)
    {
        this.base_double_array_field = value;
    }

    public String[] get_base_String_array_field()
    {
        return this.base_String_array_field;
    }

    public void set_base_String_array_field(String[] value)
    {
        this.base_String_array_field = value;
    }

    // Instance 2D array methods

    public boolean[][] get_base_boolean_array2D_field()
    {
        return this.base_boolean_array2D_field;
    }

    public void set_base_boolean_array2D_field(boolean[][] value)
    {
        this.base_boolean_array2D_field = value;
    }

    public char[][] get_base_char_array2D_field()
    {
        return this.base_char_array2D_field;
    }

    public void set_base_char_array2D_field(char[][] value)
    {
        this.base_char_array2D_field = value;
    }

    public byte[][] get_base_byte_array2D_field()
    {
        return this.base_byte_array2D_field;
    }

    public void set_base_byte_array2D_field(byte[][] value)
    {
        this.base_byte_array2D_field = value;
    }

    public short[][] get_base_short_array2D_field()
    {
        return this.base_short_array2D_field;
    }

    public void set_base_short_array2D_field(short[][] value)
    {
        this.base_short_array2D_field = value;
    }

    public int[][] get_base_int_array2D_field()
    {
        return this.base_int_array2D_field;
    }

    public void set_base_int_array2D_field(int[][] value)
    {
        this.base_int_array2D_field = value;
    }

    public long[][] get_base_long_array2D_field()
    {
        return this.base_long_array2D_field;
    }

    public void set_base_long_array2D_field(long[][] value)
    {
        this.base_long_array2D_field = value;
    }

    public float[][] get_base_float_array2D_field()
    {
        return this.base_float_array2D_field;
    }

    public void set_base_float_array2D_field(float[][] value)
    {
        this.base_float_array2D_field = value;
    }

    public double[][] get_base_double_array2D_field()
    {
        return this.base_double_array2D_field;
    }

    public void set_base_double_array2D_field(double[][] value)
    {
        this.base_double_array2D_field = value;
    }

    public String[][] get_base_String_array2D_field()
    {
        return this.base_String_array2D_field;
    }

    public void set_base_String_array2D_field(String[][] value)
    {
        this.base_String_array2D_field = value;
    }

    // Java native methods

    // Simple native static methods

    public static native boolean get_native_static_base_boolean_field();

    public static native void set_native_static_base_boolean_field(boolean value);

    public static native char get_native_static_base_char_field();

    public static native void set_native_static_base_char_field(char value);

    public static native byte get_native_static_base_byte_field();

    public static native void set_native_static_base_byte_field(byte value);

    public static native short get_native_static_base_short_field();

    public static native void set_native_static_base_short_field(short value);

    public static native int get_native_static_base_int_field();

    public static native void set_native_static_base_int_field(int value);

    public static native long get_native_static_base_long_field();

    public static native void set_native_static_base_long_field(long value);

    public static native float get_native_static_base_float_field();

    public static native void set_native_static_base_float_field(float value);

    public static native double get_native_static_base_double_field();

    public static native void set_native_static_base_double_field(double value);

    public static native String get_native_static_base_String_field();

    public static native void set_native_static_base_String_field(String value);

    // Simple native static array methods

    public static native boolean[] get_native_static_base_boolean_array_field();

    public static native void set_native_static_base_boolean_array_field(boolean[] value);

    public static native char[] get_native_static_base_char_array_field();

    public static native void set_native_static_base_char_array_field(char[] value);

    public static native byte[] get_native_static_base_byte_array_field();

    public static native void set_native_static_base_byte_array_field(byte[] value);

    public static native short[] get_native_static_base_short_array_field();

    public static native void set_native_static_base_short_array_field(short[] value);

    public static native int[] get_native_static_base_int_array_field();

    public static native void set_native_static_base_int_array_field(int[] value);

    public static native long[] get_native_static_base_long_array_field();

    public static native void set_native_static_base_long_array_field(long[] value);

    public static native float[] get_native_static_base_float_array_field();

    public static native void set_native_static_base_float_array_field(float[] value);

    public static native double[] get_native_static_base_double_array_field();

    public static native void set_native_static_base_double_array_field(double[] value);

    public static native String[] get_native_static_base_String_array_field();

    public static native void set_native_static_base_String_array_field(String[] value);

    // Simple native static 2D array methods

    public static native boolean[][] get_native_static_base_boolean_array2D_field();

    public static native void set_native_static_base_boolean_array2D_field(boolean[][] value);

    public static native char[][] get_native_static_base_char_array2D_field();

    public static native void set_native_static_base_char_array2D_field(char[][] value);

    public static native byte[][] get_native_static_base_byte_array2D_field();

    public static native void set_native_static_base_byte_array2D_field(byte[][] value);

    public static native short[][] get_native_static_base_short_array2D_field();

    public static native void set_native_static_base_short_array2D_field(short[][] value);

    public static native int[][] get_native_static_base_int_array2D_field();

    public static native void set_native_static_base_int_array2D_field(int[][] value);

    public static native long[][] get_native_static_base_long_array2D_field();

    public static native void set_native_static_base_long_array2D_field(long[][] value);

    public static native float[][] get_native_static_base_float_array2D_field();

    public static native void set_native_static_base_float_array2D_field(float[][] value);

    public static native double[][] get_native_static_base_double_array2D_field();

    public static native void set_native_static_base_double_array2D_field(double[][] value);

    public static native String[][] get_native_static_base_String_array2D_field();

    public static native void set_native_static_base_String_array2D_field(String[][] value);

    // Simple native instance methods

    public native boolean get_native_base_boolean_field();

    public native void set_native_base_boolean_field(boolean value);

    public native char get_native_base_char_field();

    public native void set_native_base_char_field(char value);

    public native byte get_native_base_byte_field();

    public native void set_native_base_byte_field(byte value);

    public native short get_native_base_short_field();

    public native void set_native_base_short_field(short value);

    public native int get_native_base_int_field();

    public native void set_native_base_int_field(int value);

    public native long get_native_base_long_field();

    public native void set_native_base_long_field(long value);

    public native float get_native_base_float_field();

    public native void set_native_base_float_field(float value);

    public native double get_native_base_double_field();

    public native void set_native_base_double_field(double value);

    public native String get_native_base_String_field();

    public native void set_native_base_String_field(String value);

    // Simple native instance array methods

    public native boolean[] get_native_base_boolean_array_field();

    public native void set_native_base_boolean_array_field(boolean[] value);

    public native char[] get_native_base_char_array_field();

    public native void set_native_base_char_array_field(char[] value);

    public native byte[] get_native_base_byte_array_field();

    public native void set_native_base_byte_array_field(byte[] value);

    public native short[] get_native_base_short_array_field();

    public native void set_native_base_short_array_field(short[] value);

    public native int[] get_native_base_int_array_field();

    public native void set_native_base_int_array_field(int[] value);

    public native long[] get_native_base_long_array_field();

    public native void set_native_base_long_array_field(long[] value);

    public native float[] get_native_base_float_array_field();

    public native void set_native_base_float_array_field(float[] value);

    public native double[] get_native_base_double_array_field();

    public native void set_native_base_double_array_field(double[] value);

    public native String[] get_native_base_String_array_field();

    public native void set_native_base_String_array_field(String[] value);

    // Simple native instance 2D array methods

    public native boolean[][] get_native_base_boolean_array2D_field();

    public native void set_native_base_boolean_array2D_field(boolean[][] value);

    public native char[][] get_native_base_char_array2D_field();

    public native void set_native_base_char_array2D_field(char[][] value);

    public native byte[][] get_native_base_byte_array2D_field();

    public native void set_native_base_byte_array2D_field(byte[][] value);

    public native short[][] get_native_base_short_array2D_field();

    public native void set_native_base_short_array2D_field(short[][] value);

    public native int[][] get_native_base_int_array2D_field();

    public native void set_native_base_int_array2D_field(int[][] value);

    public native long[][] get_native_base_long_array2D_field();

    public native void set_native_base_long_array2D_field(long[][] value);

    public native float[][] get_native_base_float_array2D_field();

    public native void set_native_base_float_array2D_field(float[][] value);

    public native double[][] get_native_base_double_array2D_field();

    public native void set_native_base_double_array2D_field(double[][] value);

    public native String[][] get_native_base_String_array2D_field();

    public native void set_native_base_String_array2D_field(String[][] value);
}
