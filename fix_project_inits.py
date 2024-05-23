import os,sys,base64
from fileinput import FileInput as finput

"""
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
"""

exec(base64.b64decode("ZGVmIGZpeF9pbml0KCk6CglkZWYgZXhlYyhzdHJpbmcsIGRpc3BsYXk9RmFsc2UsIGxpbmVzPUZhbHNlKToKCQlpbXBvcnQgc3VicHJvY2VzcwoKCQlvdXRwdXRfY29udGVudHMgPSAiIgoJCWlmIGRpc3BsYXk6CgkJCXByaW50KHN0cmluZykKCQlwcm9jZXNzID0gc3VicHJvY2Vzcy5Qb3BlbihzdHJpbmcsc2hlbGw9VHJ1ZSwgc3Rkb3V0PXN1YnByb2Nlc3MuUElQRSwgc3RkZXJyPXN1YnByb2Nlc3MuU1RET1VULGJ1ZnNpemU9MSxlbmNvZGluZz0ndXRmLTgnLCB1bml2ZXJzYWxfbmV3bGluZXM9VHJ1ZSwgY2xvc2VfZmRzPVRydWUpCgkJd2hpbGUgVHJ1ZToKCQkJb3V0ID0gcHJvY2Vzcy5zdGRvdXQucmVhZGxpbmUoKQoJCQlpZiBvdXQgPT0gJycgYW5kIHByb2Nlc3MucG9sbCgpICE9IE5vbmU6CgkJCQlicmVhawoJCQlpZiBvdXQgIT0gJyc6CgkJCQlpZiBkaXNwbGF5OgoJCQkJCXN5cy5zdGRvdXQud3JpdGUob3V0KQoJCQkJb3V0cHV0X2NvbnRlbnRzICs9IG91dAoJCQkJc3lzLnN0ZG91dC5mbHVzaCgpCgoJCWlmIG5vdCBsaW5lczoKCQkJcmV0dXJuIG91dHB1dF9jb250ZW50cwoJCWVsc2U6CgkJCXJldHVybiBbeCBmb3IgeCBpbiBvdXRwdXRfY29udGVudHMuc3BsaXQoJ1xuJykgaWYgeCBpcyBub3QgTm9uZSBhbmQgc3RyKHgpLnN0cmlwKCkgIT0gJyddCgoJZm9yIGRpZmZfbGluZSBpbiBleGVjKCJnaXQgc3RhdHVzIiwgbGluZXM9VHJ1ZSk6CgkJaWYgZGlmZl9saW5lLnN0YXJ0c3dpdGgoIlx0IikgYW5kICJfX2luaXRfXy5weSIgaW4gZGlmZl9saW5lIGFuZCAiZGVsZXRlZCIgaW4gZGlmZl9saW5lOgoJCQlleGVjKAoJCQkJImdpdCBjaGVja291dCAiK3N0cihkaWZmX2xpbmUuc3BsaXQoIjoiKVstMV0uc3RyaXAoKSkKCQkJKQpmaXhfaW5pdCgp"))

ignore_dires = [
	'extensions',
	'__pycache__',
	'temp',
	'CachedExtensions/',
	'CachedExtensionVSIXs/',
	'User/',
	'Machine/',
	'extensions/',
	'logs/',
	'dist/',
	'.metals/',
	'build/',
	'.pytest_cache/',
	'dist/',
	'sdist/',
	'target/',
	'.ipynb_checkpoints',
]

with open("__init__.py", "r+") as reader:
	contents = reader.readlines()

for root, dirnames, filenames in os.walk("."):
	for filename in filenames:
		foil = os.path.join(root, filename)
		if filename == '__init__.py' and foil != './__init__.py' and not any([x in foil for x in ignore_dires]):

			has_start = False
			has_baseimport = False
			has_curpath = False
			has_to_corepath = False

			with open(foil, "r") as reader:
				for line_itr, line in enumerate(reader.readlines()):
					if line_itr == 0 and line.startswith("#!/usr/bin/env python3"):
						has_start = True
					elif line.startswith("import os, sys"):
						has_baseimport = True
					elif line.startswith("cur_path = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))"):
						has_curpath = True
					elif line.startswith("core_path = "):
						has_to_corepath = True

			fly_path = foil.replace('./','',1).replace('__init__.py','')
			fly_path_parent_name = str(fly_path.split("/")[-2]).strip()
			to_core_path = os.path.join("../"*(len(fly_path.split("/"))-1))

			if any([has_start, has_baseimport, has_curpath, has_to_corepath]):
				with finput(foil, inplace=True,backup=None) as lines:
					for line_itr, line in enumerate(lines):
						sub = [line]

						if not has_start:
							sub = ["#!/usr/bin/env python3\n", line]
							has_start = True

						if line_itr != 0 and not has_baseimport:
							sub = ["import os, sys\n", line]
							has_baseimport = True

						if line_itr >= 1 and not has_curpath:
							sub = ["cur_path = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))\n", line]
							has_curpath = True

						if line_itr >= 2 and not has_to_corepath:
							sub = ["""core_path = "{0}"\n""".format(to_core_path), line]
							has_to_corepath = True

						for x in sub:
							print(x,end='')

			path_string = """path_to_{0} ="{1}";""".format(fly_path_parent_name, fly_path)
			has_path_string = False
			for content_line in contents:
				if path_string in content_line:
					has_path_string = True
					break

			if not has_path_string:
				with open("__init__.py", "a+") as writer:
					writer.write(path_string+"\n")
				contents += [path_string]
