import os,sys

def run(string):
	try:
		print(string)
		os.system(string)
	except Exception as e:
		print(e)

"""
* https://stackoverflow.com/questions/65149373/kernel-driver-not-installed-rc-1908-getting-errors-in-macos-big-sur-11-0-
* https://www.youtube.com/watch?v=Ftj0LvzN5Cw
"""

def getArgs():
	import argparse
	parser = argparse.ArgumentParser("VB Fix")
	parser.add_argument("-s","--step", help="setup git creds",nargs=1, default=None)
	return parser.parse_args()

if __name__ == '__main__':
	args = getArgs()
	steps = []
	if args.step:
		step = str(args.step[0])
		if step == "1":
			steps += ["sudo kextload -b org.virtualbox.kext.VBoxDrv"]
		if step == "1" or step == "2":
			steps += ['open "x-apple.systempreferences:com.apple.preference.security"']
		if step == "1" or step == "2" or step == "3":
			steps += ["sudo kextload -b org.virtualbox.kext.VBoxNetFlt"]
			steps += ["sudo kextload -b org.virtualbox.kext.VBoxNetAdp"]
			steps += ["sudo kextload -b org.virtualbox.kext.VBoxUSB"]
		if step == "1" or step == "2" or step == "3" or step == "4":
			steps += ["sudo reboot -h now"]
	for step in steps:
		run(step)