import os,sys,json
from copy import deepcopy as dc

def run(string):
	print(string)
	os.system(string)


class Color(object):
	"""
	reference from https://gist.github.com/Jossef/0ee20314577925b4027f and modified bit.
	"""

	def __init__(self, text, **user_styles):

		styles = {
			# styles
			'reset': '\033[0m',
			'bold': '\033[01m',
			'disabled': '\033[02m',
			'underline': '\033[04m',
			'reverse': '\033[07m',
			'strike_through': '\033[09m',
			'invisible': '\033[08m',
			# text colors
			'fg_black': '\033[30m',
			'fg_red': '\033[31m',
			'fg_green': '\033[32m',
			'fg_orange': '\033[33m',
			'fg_blue': '\033[34m',
			'fg_purple': '\033[35m',
			'fg_cyan': '\033[36m',
			'fg_light_grey': '\033[37m',
			'fg_dark_grey': '\033[90m',
			'fg_light_red': '\033[91m',
			'fg_light_green': '\033[92m',
			'fg_yellow': '\033[93m',
			'fg_light_blue': '\033[94m',
			'fg_pink': '\033[95m',
			'fg_light_cyan': '\033[96m',
			'fg_white': '\033[97m',
			'fg_default': '\033[99m',
			# background colors
			'bg_black': '\033[40m',
			'bg_red': '\033[41m',
			'bg_green': '\033[42m',
			'bg_orange': '\033[43m',
			'bg_blue': '\033[44m',
			'bg_purple': '\033[45m',
			'bg_cyan': '\033[46m',
			'bg_light_grey': '\033[47m'
		}

		self.color_text = ''
		for style in user_styles:
			try:
				self.color_text += styles[style]
			except KeyError:
				raise KeyError('def color: parameter `{}` does not exist'.format(style))

		self.color_text += text

	def __format__(self):
		return '\033[0m{}\033[0m'.format(self.color_text)

	@classmethod
	def red(clazz, text):
		cls = clazz(text, bold=True, fg_red=True)
		return cls.__format__()

	@classmethod
	def orange(clazz, text):
		cls = clazz(text, bold=True, fg_orange=True)
		return cls.__format__()

	@classmethod
	def green(clazz, text):
		cls = clazz(text, bold=True, fg_green=True)
		return cls.__format__()

	@classmethod
	def custom(clazz, text, **custom_styles):
		cls = clazz(text, **custom_styles)
		return cls.__format__()

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

#BFG Just in Case
#https://rtyley.github.io/bfg-repo-cleaner/

user_file = "/tmp/.ezgit.json"

def getArgs():
	import argparse
	parser = argparse.ArgumentParser("Git EZ Aide")
	parser.add_argument("-l","--login", help="setup git creds",nargs=1, default=None)
	parser.add_argument("-f","--full", help="Start an ssh agent and add cert",nargs=1, default=None)
	parser.add_argument("-o","--file", help="Update single file",nargs=1, default=None)
	parser.add_argument("-m","--message",help="The message to commit with and push", nargs="?", default=None)
	parser.add_argument("-s","--status", action="store_true",default=False, help="Show the status of the repo")
	parser.add_argument("--backward", action="store_true",default=False, help="Undo the most recent git commit")
	parser.add_argument("--reset", action="store_true",default=False, help="Reset the current repo to the remote repo")
	parser.add_argument("-a","--agent", action="store_true",default=False, help="Run the agent")
	parser.add_argument("-c","--cert", help="Add the certificate",nargs=1, default=None)
	parser.add_argument("-u","--user", help="Set the user name",nargs=1, default=None)
	parser.add_argument("-g","--clone", help="Clone a repo from the saved user name",nargs=1, default=None)
	parser.add_argument("-z","--certz", help="Add the certificates from within ~/.ssh",action="store_true",default=False,)
	parser.add_argument("-b","--branch", nargs=1,default=None, help="checkout the specified branch")
	parser.add_argument("-p","--pull", action="store_true",default=False, help="Run a git pull")
	parser.add_argument("--sub", help="Add a submodule to the current directory",nargs=1, default=None)
	parser.add_argument("--safe", help="Globally trust a repo",nargs=1, default=None)
	parser.add_argument("--upsub", action="store_true",default=False, help="Update the submodules")
	parser.add_argument("--wipe", action="store_true",default=False, help="Run a git history wipe")
	parser.add_argument("--noFlow", action="store_true",default=False, help="Run a git actions flow history wipe (has to be disabled manually)")
	parser.add_argument("--chmod", action="store_true",default=False, help="Reset the chmod changes")
	parser.add_argument("--init", action="store_true",default=False, help="Reset the odd __init__ file changes")
	return parser.parse_args()

if __name__ == '__main__':
	"""
	SubModules:
	* https://www.vogella.com/tutorials/GitSubmodules/article.html
	* https://git-scm.com/docs/git-submodule
	* https://git-scm.com/book/en/v2/Git-Tools-Submodules
	"""
	args = getArgs()
	if args.login:
		run("git config --global user.email \"{0}\"".format(args.login[0]))
		run("git config --global user.name \"{0}\"".format(args.login[0].split('@')[0]))
		with open("/tmp/.ezgit.txt", "w+") as writer:
			writer.write(args.login[0].split('@')[0])
	if args.user:
		if os.path.exists(user_file):
			os.remove(user_file)
		run("touch {0}".format(user_file))
		with open(user_file,"w+") as writer:
			json.dump({
				"user":args.user[0]
			},writer)
		run("git status")
	if args.safe:
		run("git config --global --add safe.directory {0}".format(args.safe[0]))
	if args.chmod:
		try:
			import mystring
		except:
			os.system("{0} -m pip install --upgrade mystring".format(sys.executable))
			import mystring

		for foil_line in mystring.string("git status").exec(display=False,lines=True):
			foil_line = foil_line.strip()
			if foil_line.startswith("modified"):
				foil_line = foil_line.replace("modified:","").strip()
				foil_diff = mystring.string("git diff {0}".format(foil_line)).exec(display=False, lines=True)
				if len(foil_diff) == 3 and foil_diff[1].startswith("old mode") and foil_diff[2].startswith("new mode"):
					mystring.string("git checkout {0}".format(foil_line)).exec(display=False)
			print(".",end='',flush=True)
	if args.status:
		try:
			import mystring
		except:
			os.system("{0} -m pip install --upgrade mystring".format(sys.executable))
			import mystring

		for foil_line in mystring.string("git status").exec(display=False,lines=True):
			line_to_display = None
			og_foil_loine = dc(foil_line)
			foil_line = foil_line.strip()
			if foil_line.startswith("modified"):
				foil_line = foil_line.replace("modified:","").strip()
				foil_diff = mystring.string("git diff {0}".format(foil_line)).exec(display=False, lines=True)
				if len(foil_diff) == 3 and foil_diff[1].startswith("old mode") and foil_diff[2].startswith("new mode"):
					pass
				else:
					line_to_display = og_foil_loine
			else:
				line_to_display = og_foil_loine

			if line_to_display:
				if "/" in line_to_display and "." in line_to_display and "Your branch is up to date" not in line_to_display and "git add/rm" not in line_to_display:
					if "deleted:" in og_foil_loine:
						print(Color.custom(og_foil_loine, bold=True, fg_red=True), end='\n',flush=True)
					elif "modified:" in og_foil_loine:
						print(Color.custom(og_foil_loine, bold=True, fg_blue=True), end='\n',flush=True)
					else:
						print(Color.custom(og_foil_loine, bold=True, fg_green=True), end='\n',flush=True)
				else:
					print(og_foil_loine, end='\n',flush=True)
	if args.backward:
		run("git reset --soft HEAD~1")
	if args.init:
		for diff_line in exec("git status", lines=True):
			if diff_line.startswith("\t") and "__init__.py" in diff_line and "deleted" in diff_line:
				exec(
					"git checkout "+str(diff_line.split(":")[-1].strip())
				)
		"""
		exec(base64.b64decode("ZGVmIGZpeF9pbml0KCk6CglkZWYgZXhlYyhzdHJpbmcsIGRpc3BsYXk9VHJ1ZSwgbGluZXM9RmFsc2UpOgoJCWltcG9ydCBzdWJwcm9jZXNzCgoJCW91dHB1dF9jb250ZW50cyA9ICIiCgkJaWYgZGlzcGxheToKCQkJcHJpbnQoc3RyaW5nKQoJCXByb2Nlc3MgPSBzdWJwcm9jZXNzLlBvcGVuKHN0cmluZyxzaGVsbD1UcnVlLCBzdGRvdXQ9c3VicHJvY2Vzcy5QSVBFLCBzdGRlcnI9c3VicHJvY2Vzcy5TVERPVVQsYnVmc2l6ZT0xLGVuY29kaW5nPSd1dGYtOCcsIHVuaXZlcnNhbF9uZXdsaW5lcz1UcnVlLCBjbG9zZV9mZHM9VHJ1ZSkKCQl3aGlsZSBUcnVlOgoJCQlvdXQgPSBwcm9jZXNzLnN0ZG91dC5yZWFkbGluZSgpCgkJCWlmIG91dCA9PSAnJyBhbmQgcHJvY2Vzcy5wb2xsKCkgIT0gTm9uZToKCQkJCWJyZWFrCgkJCWlmIG91dCAhPSAnJzoKCQkJCWlmIGRpc3BsYXk6CgkJCQkJc3lzLnN0ZG91dC53cml0ZShvdXQpCgkJCQlvdXRwdXRfY29udGVudHMgKz0gb3V0CgkJCQlzeXMuc3Rkb3V0LmZsdXNoKCkKCgkJaWYgbm90IGxpbmVzOgoJCQlyZXR1cm4gb3V0cHV0X2NvbnRlbnRzCgkJZWxzZToKCQkJcmV0dXJuIFt4IGZvciB4IGluIG91dHB1dF9jb250ZW50cy5zcGxpdCgnXG4nKSBpZiB4IGlzIG5vdCBOb25lIGFuZCBzdHIoeCkuc3RyaXAoKSAhPSAnJ10KCglmb3IgZGlmZl9saW5lIGluIGV4ZWMoImdpdCBzdGF0dXMiLCBsaW5lcz1UcnVlKToKCQlpZiBkaWZmX2xpbmUuc3RhcnRzd2l0aCgiXHQiKSBhbmQgIl9faW5pdF9fLnB5IiBpbiBkaWZmX2xpbmUgYW5kICJkZWxldGVkIiBpbiBkaWZmX2xpbmU6CgkJCWV4ZWMoCgkJCQkiZ2l0IGNoZWNrb3V0ICIrc3RyKGRpZmZfbGluZS5zcGxpdCgiOiIpWy0xXS5zdHJpcCgpKQoJCQkpCmZpeF9pbml0KCk="))
		"""
	if args.reset:
		run("git reset --hard origin/master")
	if args.branch:
		run("git checkout {0}".format(args.branch[0]))
	if args.agent or args.full:
		run("ssh-agent /bin/bash")
	if args.certz or args.full:
		from glob import glob as re
		for cert in re(os.path.join(os.path.expanduser("~"), ".ssh", "*")):
			run("chmod 600 {cert} && ssh-add {cert}".format(cert=cert))
	if args.cert or args.full:
		cert = str(args.cert[0] or args.full[0]).strip()
		run("chmod 600 {cert} && ssh-add {cert}".format(cert=cert))
	if args.pull:
		run("git pull")
	if args.sub:
		run("git submodule add -b master {0}".format(args.sub[0].strip()))
	if args.upsub:
		run("git submodule update --remote")
	if args.message:
		run("git add .")
		run("git commit -m \"{msg}\"".format(msg=''.join(args.message)))
		run("git push")
	if args.clone:
		if os.path.exists(user_file):
			with open(user_file, "r") as reader:
				username = json.load(reader)["user"]
		else:
			with open("/tmp/.ezgit.txt", "r") as reader:
				username = reader.readlines()[0].strip()
		run("git clone git@github.com:"+str(username)+"/"+str(args.clone[0]))
	if args.file:
		run("git add {0}".format(args.file[0]))
		run("git commit -m \"Updating the file {0}\"".format(args.file[0]))
		run("git push")
	if args.wipe:
		# https://stackoverflow.com/questions/13716658/how-to-delete-all-commit-history-in-github
		for arg in [
			"git checkout --orphan latest_branch",
			"git add -A",
			'git commit -am "Initial Commit"',
			"git branch -D master",
			"git branch -m master",
			"git push -f origin master",
			"git push --set-upstream origin master"
		]:
			run(arg)
	if args.noFlow:
		#https://stackoverflow.com/questions/57927115/delete-a-workflow-from-github-actions
		run("""user=GH_USERNAME repo=REPO_NAME; gh api repos/$user/$repo/actions/runs --paginate -q '.workflow_runs[] | select(.head_branch != "master") | "\(.id)"' | xargs -n1 -I % gh api repos/$user/$repo/actions/runs/% -X DELETE """)