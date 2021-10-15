import sys, pathlib
sys.path[0] = str(pathlib.Path(__file__).resolve().parents[1])
del sys, pathlib
__import__("runpy").run_module("tests")
