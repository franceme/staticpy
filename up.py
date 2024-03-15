import os,sys

if "pip" in " ".join(sys.argv):
    os.system("{0} <(curl -sL https://bootstrap.pypa.io/get-pip.py)".format(sys.executable))

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
    "pyplotlib",
    "torrentp",
    "pnostic",
    "pip",
    "jupyter",
    "notebook",
    "jupyterlab",
    "jupyterlite",
    "ipywidgets",
    "voila",
    "voici"
]

os.system("{0} -m pip install --upgrade {1}".format(sys.executable, '  '.join(x)))