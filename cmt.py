#!/usr/bin/env python3
import os,sys

def run(string):
	print(string)
	os.system(string)

def getArgs():
	import argparse
	parser = argparse.ArgumentParser("Cmt")
	parser.add_argument("--foil", help="setup git creds",nargs=1, default=None)
	parser.add_argument("-f","--fromLine", help="The from line",nargs=1, default=None)
	parser.add_argument("-t","--toLine", help="The two line",nargs=1, default=None)
	parser.add_argument("-c","--comment", nargs=1,default="////", help="The comment type")
	parser.add_argument("-r","--remove", action="store_true",default=False, help="Remove comments if applied")
	return parser.parse_args()

def cmt(file, fromLine,toLine,comment,remove=False):
	import os,sys
	from fileinput import FileInput as finput
	if os.path.exists(file):
		with finput(file, inplace=True, backup=None) as foil:
			for lineItr, line in enumerate(foil):
				if fromLine <= lineItr < toLine:
					if line.strip().startswith(comment) and remove:
						prefix = line.replace(line.strip(),'')
						line = prefix + line.strip().replace(comment, '')
					elif not line.strip().startswith(comment) and not remove:
						line = comment+line
				print(line,end='')

if __name__ == '__main__':
	args = getArgs()
	foil = str(args.foil[0])
	if os.path.exists(foil):
		cmt(
			foil,
			fromLine=int(args.fromLine[0]),
			toLine=int(args.toLine[0]),
			comment=str(args.comment[0]),
			remove=args.remove
		)