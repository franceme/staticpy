#!/usr/bin/env python3
import os,sys

def fix_init():
	def exec(string, display=True, lines=False):
		import subprocess

		output_contents = ""
		if display:
			print(string)
		process = subprocess.Popen(string,shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,bufsize=1,encoding='utf-8', universal_newlines=True, close_fds=True)
		while True:
			out = process.stdout.readline()
			if out == '' and process.poll() != None:
				break
			if out != '':
				if display:
					sys.stdout.write(out)
				output_contents += out
				sys.stdout.flush()

		if not lines:
			return output_contents
		else:
			return [x for x in output_contents.split('\n') if x is not None and str(x).strip() != '']

	for diff_line in exec("git status", lines=True):
		if diff_line.startswith("\t") and "__init__.py" in diff_line and "deleted" in diff_line:
			exec(
				"git checkout "+str(diff_line.split(":")[-1].strip())
			)
fix_init()