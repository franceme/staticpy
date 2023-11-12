import os,sys
from abc import ABC, abstractmethod
from glob import glob as re

def run(string):
	print(string);os.system(string)

try:
	import xpiz
except:
	run("{0} -m pip install --upgrade xpiz".format(sys.executable))
	import xpiz

def getArgs():
	import argparse
	parser = argparse.ArgumentParser("Create the xpizr wrapper")
	parser.add_argument("-f","--foil", help="The file to be wrapped",nargs=1, default=None)
	parser.add_argument("-g","--github", help="The github repo to be auto-inserted to",nargs=1, default=None)
	parser.add_argument("-p","--plain", help="Just Create the python script",action='store_true',default=False)
	return parser.parse_args()

class Structure(ABC):
	def __init__(self):
		super().__init__()

	@abstractmethod
	def initString(self):
		pass

	@abstractmethod
	def getDownloadString(self):
		pass

class GitHub(Structure):
	def __init__(self, repoPath:str, repoToken:str=None):
		super().__init__()
		self.repoPath = repoPath
		self.repoToken = repoToken

	def initString(self):
		return """
try:
	import hugg
except:
	run("{{0}} -m pip install --upgrade hugg".format(sys.executable))
	import hugg
repo = hugg.ghub(
	repo="{repoPath}",
	access_token="{repoToken}",
	branch="master"
)
""".format(repoPath=self.repoPath,repoToken=self.repoToken)

	def getDownloadString(self):
		return """
def download(repoPath,file,hash):
	repo.download(file_path=repoPath, download_to=file)
	if xpiz.hash(file) != hash:
		print("The file does not equal to its hash")
	return file
"""

class GDownload(Structure):
	def __init__(self):
		super().__init__()

	def initString(self):
		return """
try:
	import gdown
except:
	run("{{0}} -m pip install --upgrade gdown".format(sys.executable))
	import gdown
"""

	def getDownloadString(self):
		return """
def download(url,file,hash):
	gdown.download(url,file,quiet=False,fuzzy=True,verify=True)
	if xpiz.hash(file) != hash:
		print("The file does not equal to its hash")
	return file
"""

def structure(fileName,fileContents,hash,githubRepo:str=None):
	if githubRepo:
		mgr = GitHub(githubRepo)
	else:
		mgr = GDownload()

	return """#!/usr/bin/env python
import os,sys
from glob import glob as re

fileName = "{fileName}"
ogHash = "{hash}"

try:
	import xpiz
except:
	run("{{0}} -m pip install --upgrade hugg".format(sys.executable))
	import xpiz

{initString}

def run(string,tryFail=False):
	print(string)
	if tryFail:
		try:
			os.system(string)
		except:
			pass
	else:
		os.system(string)

{downloadString}

def info():
	\"\"\"
	{{
		"file_name":{{
			"url":"https://...",
			"hash":"..."
		}},
		"file_name2":{{
			"url":"https://...",
			"hash":"..."
		}},
		...
	}}
	\"\"\"
	return {fileContents}

def getArgs():
	import argparse
	parser = argparse.ArgumentParser("XPizr for {fileName}")
	parser.add_argument("-d","--download", action="store_true",default=False, help="Download the file")
	parser.add_argument("-c","--clean", action="store_true",default=False, help="Clean the files")
	return parser.parse_args()

def downloading():
	for key,value in info().items():
		print(key)
		print(download(value['url'], key, value['hash']))
		verified = "===" if xpiz.hash(key) == value['hash'] else "=!="
		print("The old hash {{0}} the new hash".format(verified))
	xpiz.join(fileName)
	verified = "===" if xpiz.hash(fileName) == ogHash else "=!="
	print("The old hash {{0}} the new hash".format(verified))
	if verified:
		for foil in re("{{0}}_*".format(fileName)):
			os.remove(foil)
		os.remove(fileName+".sums")
	return fileName

if __name__ == '__main__':
	args = getArgs()
	if args.download:
		downloading()
	elif args.clean:
		run("rm {{0}}".format(fileName), True)
""".format(
	fileName=fileName,
	fileContents=fileContents,
	hash=hash,
	initString=mgr.initString(),
	downloadString=mgr.getDownloadString()
)

def createWrapper(foil, gitHubRepo:str=None, plain:bool=False):
	hash, info,filesCreated = None, {},[]

	if not plain:
		print("Getting the original hash")
		hash = xpiz.hash(foil)
		print("Splitting the file")
		filesCreated, info = xpiz.split(foil), {}
		print("Hashing the split files")
		for foile in filesCreated:
			info[foile] = {
				"url":"",
				"hash":xpiz.hash(foile)
			}
			print("Hashed File := {0}".format(foile))

	if gitHubRepo:
		try:
			import hugg
		except:
			run("{0} -m pip install --upgrade hugg".format(sys.executable))
			import hugg
		repo = hugg.ghub(
			repo=gitHubRepo,
			access_token=input("Please enter your github token :="),
			branch="master"
		)
		print()
		for key,value in filesCreated:
			repo.upload(key,key)
			value['url'] = key
			os.remove(key)

	with open("xpiz_"+foil+".py", "w+") as writer:
		writer.write(
			structure(
				foil,
				info,
				hash,
				gitHubRepo
			)
		)
	return foil

if __name__ == '__main__':
	args = getArgs()
	foil = str(args.foil[0]).strip()
	githubRepo = args.github[0] if args.github != None and len(args.github) >= 1 else None
	createWrapper(foil, githubRepo, args.plain)