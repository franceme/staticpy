import os,sys

x = [
    "pydbhub",
    "funbelts",
    "hasana",
    "petitext",
    "ephfile",
    "messenger-python",
    "morchest",
    "rebrandly",
    "mystring[all]",
    "carchive",
    "hugg[all]",
    "sdock[all]",
    "splunkr",
    "torrentp",
    "pnostic",
    "pip"
]

os.system("{0} -m pip install --upgrade {1}".format(sys.executable, ' '.join(x)))