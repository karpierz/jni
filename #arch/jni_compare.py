import cffi

from datadiff import diff
from pprint   import pprint

import jni.ctypes as jni_ctypes
import jni.cffi   as jni_cffi
import jni.cython as jni_cython
import jni.capi   as jni_capi

def attrs(obj): return {name: getattr(obj, name) for name in dir(obj)}

omit = [
    '__loader__',
    '__spec__',
    '__cached__',
    '__builtins__',
#    'absolute_import',
]

dir_jni_ctypes = sorted(dir(jni_ctypes))
dir_jni_cffi   = sorted(dir(jni_cffi))
dir_jni_cython = sorted(dir(jni_cython))
dir_jni_capi   = sorted(dir(jni_capi))
for name in omit:
    dir_jni_ctypes.remove(name)
    dir_jni_cffi  .remove(name)
    dir_jni_cython.remove(name)
    dir_jni_capi.remove(name)

var_jni_ctypes = attrs(jni_ctypes)
var_jni_cffi   = attrs(jni_cffi)
var_jni_cython = attrs(jni_cython)
var_jni_capi   = attrs(jni_capi)
for name in omit:
    var_jni_ctypes.pop(name, None)
    var_jni_cffi  .pop(name, None)
    var_jni_cython.pop(name, None)
    var_jni_capi  .pop(name, None)

# compare dirs

print("")
print("dir: jni_ctypes <--> jni_cffi")
print("=============================")
print(diff(dir_jni_ctypes, dir_jni_cffi, context=1))

print("")
print("dir: jni_ctypes <--> jni_cython")
print("===============================")
print(diff(dir_jni_ctypes, dir_jni_cython, context=1))

print("")
print("dir: jni_ctypes <--> jni_capi")
print("=============================")
print(diff(dir_jni_ctypes, dir_jni_capi, context=1))

exit(0)

# compare vars

print("")
print("vars: jni_ctypes <--> jni_cffi")
print("==============================")
print(diff(var_jni_ctypes, var_jni_cffi, context=1))

print("")
print("vars: jni_ctypes <--> jni_cython")
print("================================")
print(diff(var_jni_ctypes, var_jni_cython, context=1))

print("")
print("vars: jni_ctypes <--> jni_capi")
print("==============================")
print(diff(var_jni_ctypes, var_jni_capi, context=1))

#print("")
#print("var_jni_ctypes")
#print("==============")
#pprint(var_jni_ctypes)

#print("")
#print("var_jni_cffi")
#print("============")
#pprint(var_jni_cffi)

#print("")
#print("var_jni_cython")
#print("==============")
#pprint(var_jni_cython)

#print("")
#pprint(jni_ctypes.jint(2).value == 2)
#pprint(dir(jni_cffi.jint))
#pprint(jni_cffi.jint.__class__.__dict__)

#print(type(jni_cffi.jint.cname), jni_cffi.jint.cname)
#print(type(jni_cffi.jint.kind),  jni_cffi.jint.kind)
