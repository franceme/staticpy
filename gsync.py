#!/usr/bin/env python3
import os,sys

def getArgs():
	import argparse
	parser = argparse.ArgumentParser("GSync Aide")
	parser.add_argument("-m", "--message", help="The message to be used for the git commit", nargs="?", default=None)
	parser.add_argument("-e", "--email", help="Your email to be used", nargs="?", default=None)
	return parser.parse_args()

def main(args):
	def run(cmd):
		print(cmd)
		try:
			os.system(cmd)
		except Exception as e:
			print("Message := {0}".format(e))

	if args.email == None:
		run("git config --global user.email \"{0}\"".format(args.email))
		run("git config --global user.name  \"{0}\"".format(args.email.split("@")[0]))
	if args.message != None:
		run("git add .")
		run('git commit -m "{0}"'.format(args.message))
		run("git push")

if __name__ == '__main__':
	main(getArgs())