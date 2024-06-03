import os,sys

if "pip" in " ".join(sys.argv):
    os.system("{0} <(curl -sL https://bootstrap.pypa.io/get-pip.py)".format(sys.executable))

for x in [
    "PyGithub",
    "requests",
    "gett",
    "mystring[all]",
    "pydbhub",
    "funbelts",
    "hasana",
    "petitext",
    "plotly",
    "kaleido", #Used for plotly svg
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
    #"jupyter",
    "notebook",
    #"jupyterlab",
    "jupyterlite",
    "ipywidgets",
    "voila",
    "voici",
    "pygwalker",
    "monacopy",
    "python-dateutil",
    "starlark-go",# https://pypi.org/project/starlark-go/
]:
    os.system("{0} -m pip install --upgrade {1}".format(sys.executable, x))