import os
from shutil import copy
from filecmp import cmp

TARGET = "../target/"

SNIPPET_DIR = "test_templates/"


def copy_template(test, ext=".txt"):
    try:
        os.mkdir("../target")
    except:
        pass
    copy(SNIPPET_DIR + test + ".tmpl", TARGET + test + ext)


def assertEqual(test, ext=".txt"):
    if cmp(SNIPPET_DIR + test + ext, TARGET + test + ext):
        return
    raise Exception("result differs from what was expected for test %s" % test)
