import sys, os.path as osp
sys.path[0] = osp.dirname(osp.dirname(osp.abspath(__file__)))
del sys, osp
__import__("runpy").run_module("tests")
