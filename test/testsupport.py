import os
from shutil import copy


TARGET = "../target/"

SNIPPET_DIR = "test_templates/"


def copy_template(test, ext=".txt", template_ext=".tmpl"):
    try:
        os.mkdir("../target")
    except:
        pass
    copy(SNIPPET_DIR + test + template_ext, TARGET + test + ext)

def cmp(f1, f2):
    with open(f1, 'r') as fp1, open(f2, 'r') as fp2:
        content1 = "\n".join(fp1.read().splitlines())
        content2 = "\n".join(fp2.read().splitlines())
        return content1 == content2

def assertEqual(test, ext=".txt"):
    if cmp(SNIPPET_DIR + test + ext, TARGET + test + ext):
        return
    raise Exception("result differs from what was expected for test %s" % test)
