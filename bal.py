#!/usr/bin/env python3

import os,sys

def getArgs():
	import argparse
	parser = argparse.ArgumentParser("Ballerina Aide")
	parser.add_argument("--localize", help="Clone, build, localize, and remove a custom repository (since ballerina central has some problems).",nargs=1, default=None)
	parser.add_argument("--user", help="Username of github user.",nargs=1, default="franceme")
	args,unknown = parser.parse_known_args()
	return args


if __name__ == "__main__":
	args = getArgs()

	#https://ballerina.io/learn/manage-dependencies/
	if args.localize:
		for x in [
			f"""git clone git@github.com:{args.user}/{args.localize}""",
			f"""cd {args.localize} && bal pack """,
			f"""cd {args.localize} && bal push --repository local """,
			f"""yes|rm -r {args.localize}""",
		]:
			print(c);os.system(c);
		with open("Ballerina.toml", "a+") as writer:
			for line in [
				f""" """,
				f"""[[dependency]]""",
				f"""org = "{args.user}" """,
				f"""name = "{args.localize}" """,
				'version = "0.0.0"',
				'repository = "local"',
			]:
				writer.write(line)