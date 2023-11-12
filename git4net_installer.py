import os,sys

def run(string):
	print(string)
	os.system(string)


import os, sys, uuid, json
from invoke import task
from functools import lru_cache

try:
	import vermin as V
	from redbaron import RedBaron as rb
	import pydriller
	import Levenshtein
	import pathpy
	import metrics
	import mystring
	from ephfile import ephfile
	import scipy
	import gambit
	import networkx
except:
	os.system(f"{sys.executable} -m pip install --upgrade scipy vermin redbaron pydriller Levenshtein pathpy metrics mystring ephfile gambit networkx")
	import vermin as V
	import pydriller
	import Levenshtein
	import pathpy
	from redbaron import RedBaron as rb
	import metrics
	import mystring
	from ephfile import ephfile
	import gambit
	import networkx


try:
	import git2net
	import requests
except:
	os.system(f"{sys.executable} -m pip install git+https://github.com/franceme/git4net")
	os.system(f"{sys.executable} -m pip install requests")
	import site, zipfile, requests
	path = os.path.join(site.getsitepackages()[0],'git2net')
	try:
		os.rename(os.path.join(site.getsitepackages()[0],'git4net'), path)
	except: pass

	temp_file = "/tmp/helpers.zip"
	r = requests.get("https://github.com/franceme/git4net/releases/download/binary/helpers.zip", stream=True)
	with open(temp_file, 'wb') as fd:
		for chunk in r.iter_content(chunk_size=128):
			fd.write(chunk)

	with zipfile.ZipFile(temp_file, 'r') as zip_ref:
		zip_ref.extractall(path)

	os.remove(temp_file)

	import git2net

try:
	from carchive import GRepo_Seed_Metric, GRepo_Pod
except:
	os.system(f"{sys.executable} -m pip install --upgrade carchive")
	from carchive import GRepo_Seed_Metric, GRepo_Pod


"""
#Insert the following code near the top to import these relevant fun stuff
try:
	import vermin as V
	from redbaron import RedBaron as rb
	import pydriller
	import Levenshtein
	import pathpy
	import metrics
	import mystring
	from ephfile import ephfile
	import scipy
	import gambit
	import networkx
	from carchive import GRepo_Seed_Metric, GRepo_Pod
except:
	import urllib.request;temp_path="git4net_installer.py"
	urllib.request.urlretrieve("https://raw.githubusercontent.com/franceme/staticpy/master/git4net_installer.py", temp_path)
	with open(temp_path,"r") as reader:
		exec('\n'.join(reader.readlines()))
	os.remove(temp_path)

	import vermin as V
	import pydriller
	import Levenshtein
	import pathpy
	from redbaron import RedBaron as rb
	import metrics
	import mystring
	from ephfile import ephfile
	import gambit
	import networkx
	from carchive import GRepo_Seed_Metric, GRepo_Pod
"""