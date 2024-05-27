#!/usr/bin/env python3

import os,sys

def getArgs():
	import argparse
	parser = argparse.ArgumentParser("Ballerina Aide")
	parser.add_argument("--localize", help="Clone, build, localize, and remove a custom repository (since ballerina central has some problems).",nargs=1, default=None)
	parser.add_argument("--user", help="Username of github user.",nargs=1, default=["franceme"])
	parser.add_argument("--base", help="Base Path.",nargs=1, default=["/tmp"])
	parser.add_argument("--save", help="Don't delete the repository",action="store_true",default=False)
	args,unknown = parser.parse_known_args()
	return args

if __name__ == "__main__":
	args = getArgs()

	base = args.base[0].strip()
	user = args.user[0].strip()

	#https://ballerina.io/learn/manage-dependencies/
	if args.localize:
		localize = args.localize[0].strip()
		local = os.path.join(base, localize)

		cmds = []

		if not os.path.exists(os.path.join(base, localize)):
			cmds += ['cd {0} && git clone git@github.com:{1}/{2}'.format(base, user, localize)]

		cmds += ['cd {0} && bal clean'.format(local)]
		cmds += ['cd {0} && bal pack'.format(local)]
		cmds += ['cd {0} && bal push --repository local'.format(local)]

		if not args.save:
			cmds += ['yes|rm -r {0}'.format(local)]

		for x in cmds:
			print(x);os.system(x)

		if False:
			with open(os.path.join(base,"Ballerina.toml"), "a+") as writer:
				for line in [
					"",
					'[[dependency]]',
					'org = "{0}"'.format(user),
					'name = "{0}"'.format(localize),
					'version = "0.0.0"',
					'repository = "local"',
				]:
					writer.write(line+"\n")