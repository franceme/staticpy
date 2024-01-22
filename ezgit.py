import os,sys,json

def run(string):
	print(string)
	os.system(string)

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
	if args.status:
		run("git status")
	if args.backward:
		run("git reset --soft HEAD~1")
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