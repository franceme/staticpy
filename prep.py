import os,sys

contents = {}
contents["vv"] = """#!/usr/bin/env python3
import os,sys
from importlib.metadata import version
from datetime import datetime

try:
	if version('sdock') < '0.1.51':
		raise Exception("Upgrade the version")
except:
	os.system("{0} -m pip install --upgrade sdock".format(sys.executable))
from sdock.vvv import *

#Choco Packages: https://community.chocolatey.org/packages

box_name = "tempbox"
box = vagrant(
	box="talisker/windows10pro",
	name=box_name,
	provider=Provider.virtualbox(),
	disablehosttime = True,
	disablenetwork = True,
	vmdate = datetime(year=2023, month=1, day=10, hour=3, minute=0, second=0),
	python_packages = ["hugg"],
)

def getArgs():
	import argparse
	parser = argparse.ArgumentParser("Vagrant Runner for {0}".format(box_name))
	parser.add_argument("--start", help="Start the box",action='store_true',default=False)
	parser.add_argument("--stop", help="Stop the box",action='store_true',default=False)
	parser.add_argument("--clean", help="Clean the box",action='store_true',default=False)
	#parser.add_argument("--save", help="Save the progress with the box",action='store_true',default=False)
	#parser.add_argument("--load", help="Load the progress with the box",action='store_true',default=False)
	args,unknown = parser.parse_known_args()
	return args

args = getArgs()
if args.start:
	box.on()
elif args.stop:
	box.off()
elif args.clean:
	box.clean()
"""

args = " ".join(sys.argv)
for key,value in contents.items():
    if key in args:
        print("Writing the prep file for {0}".format(key), flush=True)
        with open(key+".py", "w+") as writer:
            writer.write(value)