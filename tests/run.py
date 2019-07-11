import sys, os.path as path
sys.path[0] = path.dirname(path.dirname(path.abspath(__file__)))
del sys, path
__import__("runpy").run_module("tests")
