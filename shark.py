import os,sys

# Reference
# https://serverfault.com/questions/362529/how-can-i-sniff-the-traffic-of-remote-machine-with-wireshark

def run(string, back=False):
	if back:
		string = "{0} &".format(string)
	print(string)
	os.system(string)


def pipe():
	path = "/tmp/remote"
	if not os.path.exists(path):
		run("mkfifo {0}".format(path))
	return path


def grouping():
	run("sudo chgrp wireshark /usr/sbin/tcpdump")


def shark():
	cmd = ""
	run("wireshark -k -i {0}".format(pipe()),True)


def ethdump():
	grouping()
	run("sudo tcpdump -s 0 -U -n -w - -i eth0 not port 22 > {0}".format(pipe()), True)


def lodump():
	grouping()
	run("sudo tcpdump -s 0 -U -n -w - -i lo port 5000 > {0}".format(pipe()), True)


def kill(arg):
	run("""ps -ef|grep {0}|head -n 1|awk '{{print $2}}'|xargs -I {{}} sh -c "kill {{}};" """.format(arg))


def killdump():
	kill("tcpdump")


def killshark():
	kill("wireshark")


def getArgs():
	import argparse
	parser = argparse.ArgumentParser("Wireshark Aide Py")
	parser.add_argument("--shark", help="Run WireShark",action='store_true',default=False)
	parser.add_argument("--wireshark", help="Run WireShark",action='store_true',default=False)
	parser.add_argument("--local", help="Trace Local",action='store_true',default=False)
	parser.add_argument("--eth", help="Trace Eth",action='store_true',default=False)
	parser.add_argument("--kill", help="Kill the tcpdump",action='store_true',default=False)
	parser.add_argument("--killshark", help="Kill WireShark",action='store_true',default=False)
	parser.add_argument("--flocal", help="Prep Local and run Wireshark",action='store_true',default=False)
	return parser.parse_args()

if __name__ == '__main__':
	args = getArgs()
	if args.shark or args.wireshark:
		shark()
	elif args.local:
		lodump()
	elif args.eth:
		ethdump()
	elif args.kill:
		killdump()
	elif args.killshark:
		killshark()
	elif args.flocal:
		lodump();shark()