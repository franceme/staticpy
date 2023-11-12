#!/usr/bin/env python3


'''####################################
#Version: 00.00
#Version Numbering: Major.Minor
#Reasons for imports
os		: used for verifying and reading files
sys		: used for exiting the system
python3 <(curl -sL https://rebrand.ly/pydock)
'''####################################

##Imports
import os
import sys
import subprocess
import platform
import socket
import sdock
from sdock.docker import dock

"""
sample forcing a docker container to run as su
docker run --rm -u 0 -it -v `pwd`:/temp username/dockername
 > -u 0
 > forcing the user id to be 0, the root id

Eventually switch to
https://github.com/docker/docker-py

Things to add:
* Join existing and running docker container
"""


docker_username = "frantzme"

'''####################################
#The main runner of this file, intended to be ran from
'''####################################

dir = '%cd%' if sys.platform in ['win32', 'cygwin'] else '`pwd`'
use_sudo = False

# Global Arguments
network = None
dind = False
detach = False
savedir = False
baredocker = None


def getArgs():
	global docker_username
	import argparse
	parser = argparse.ArgumentParser("DockerPush = useful utilities for running docker images")
	parser.add_argument("-x","--command", help="The Docker image to be used", nargs='*', default="clean")
	parser.add_argument("-d","--docker", help="The Docker image to be used", nargs='*', default="frantzme/pydev:latest")
	parser.add_argument("-p","--ports", help="The ports to be exposed", nargs="*", default=[])
	parser.add_argument("-c","--cmd", help="The cmd to be run", nargs="*", default=["/bin/bash"])
	parser.add_argument("-e","--extra", help="Extra info to be piped in", nargs="*", default=[])
	parser.add_argument("-r","--raw", action='append', help="Extra info to be directly added into the command", nargs="*", default=[])
	parser.add_argument("--shebang", help="", action="store_true",default=False)

	#https://stackoverflow.com/questions/42946453/how-does-the-docker-assign-mac-addresses-to-containers
	parser.add_argument("--mac", help="Set the Mac Address",default=None)

	parser.add_argument("--mount", help="mount the current directory to which virtual folder",default="/sync")
	parser.add_argument("--mountfrom", help="mount the current directory to which virtual folder",default=":!")
	parser.add_argument("-n","--name", help="The name of the image",default="kinde")
	parser.add_argument("--shared", help="Created a shared folder between docker and internal dockers.", action="store_true",default=False) #https://stackoverflow.com/questions/53539807/why-docker-in-docker-dind-containers-mount-volumes-with-host-path#answer-53542041
	parser.add_argument("--useshared", help="Used the shared point as a mounting point", action="store_true",default=False) #https://stackoverflow.com/questions/53539807/why-docker-in-docker-dind-containers-mount-volumes-with-host-path#answer-53542041
	parser.add_argument("--Login", help="Login", action="store_true",default=False)
	parser.add_argument("--Logout", help="Logout", action="store_true",default=False)
	parser.add_argument("--Logg", help="Login and Logout", action="store_true",default=False)
	parser.add_argument("--execute", help="Execute the script (default is True)", action="store_false",default=True)
	parser.add_argument("--short1", action="store_true",default=False, help=argparse.SUPPRESS)
	parser.add_argument("--short2", action="store_true",default=False, help=argparse.SUPPRESS)
	parser.add_argument("--short3", action="store_true",default=False, help=argparse.SUPPRESS)
	parser.add_argument("--vs", action="store_true",default=False, help=argparse.SUPPRESS)
	parser.add_argument("--shorty", action="store_true",default=False, help=argparse.SUPPRESS)
	parser.add_argument("--makerust", action="store_true",default=False, help=argparse.SUPPRESS)
	parser.add_argument("--grace", action="store_true",default=False, help=argparse.SUPPRESS)
	parser.add_argument("--graceExt", action="store_true",default=False, help=argparse.SUPPRESS)
	parser.add_argument("--graceLogs", action="store_true",default=False, help=argparse.SUPPRESS)
	args,unknown = parser.parse_known_args()
	return args

def setGlobalArgs():
	import argparse
	parser = argparse.ArgumentParser("Global Grabber")
	parser.add_argument("--network", help="The network option to be used", nargs='*', default=None)
	parser.add_argument("--dind", help="Use Docker In Docker", action="store_true", default=False)
	parser.add_argument("--detach", help="Run the docker imagr detached", action="store_true",default=False)
	parser.add_argument("--savedir", help="Save the base directory to the docker", action="store_true",default=False)
	parser.add_argument("--sudo", help="Add sudo onto docker", action="store_true",default=False)
	parser.add_argument("--baredocker", help="Don't use the bare docker name provided: {}".format(docker_username), action="store_true",default=False)

	args, _ = parser.parse_known_args()
	argz = ' '.join(sys.argv)

	global network
	if args.network and network is None:
		network = args.network[0]
		argz = argz.replace("--network {0}".format(network),"")

	global use_sudo
	if args.sudo:
		use_sudo = True
		argz = argz.replace("--sudo","")

	global dind
	if args.dind:
		dind = True
		argz = argz.replace("--dind","")

	global detach
	if args.detach:
		detach = True
		argz = argz.replace("--detach","")

	global savedir
	if args.savedir:
		savedir = True
		argz = argz.replace("--savedir","")

	global baredocker
	if args.baredocker:
		baredocker = True
		argz = argz.replace("--baredocker","")

	sys.argv = argz.split(" ")
	return args

def flatten_list(lyst: list) -> list:
	if not lyst:
		return []

	big_list = len(lyst) > 1
	if isinstance(lyst[0], list):
		return flatten_list(lyst[0]) + (big_list * flatten_list(lyst[1:]))
	else:
		return [lyst[0]] + (big_list * flatten_list(lyst[1:]))

def duel_cmd(first_cmd, second_cmd):
	global docker
	output = []

	for image in cmd("{0} {1}".format(docker, first_cmd), lines=True, display=False):
		output += [
			"{0} {1} {2}".format(docker, second_cmd, image)
		]

	#cmds.append(duel_cmd("images -q","rmi"))
	return output

def base_dock(
		dockerName, # [X]
		ports=[], # [X]
		flags="", # [X]
		mount="/sync", # [X]
		cmd="/bin/bash", # [X]
		args="", # [ ]
		raw="",
		mac=None, # [X]
		extra='' # [X]
	):
	global use_sudo
	global network
	global dind
	global detach
	global savedir
	global baredocker

	return dock(
		#docker = "docker",
		image = sdock.docker.dock.dockerImage(dockerName,baredocker),
		ports = ports,
		cmd = cmd,
		network = network,
		dind = dind,
		shared = False,
		detach = detach,
		sudo = use_sudo,
		remove = True,
		mountto = "/sync",
		mountfrom = mount,
		name = "current_running",
		login = False,
		loggout = False,
		logg = False,
		macaddress = mac,
		raw=raw,
		postClean = False,
		preClean = False,
		extra = args + ' ' + extra.replace('"','').replace("'",'') + ' '.join(flags),
		save_host_dir = savedir,
	)

def base_run(
		dockerName, # [X]
		ports=[], # [X]
		flags="", # [X]
		mount="/sync", # [X]
		cmd="/bin/bash", # [X]
		args="", # [ ]
		raw=[],
		mac=None, # [X]
		extra='' # [X]
	):

	if len(raw) > 0:
		argr = str(' '.join([x[0].replace('"',"").replace("'",'') for x in raw])).strip()
	else:
		argr = ""

	return base_dock(
		dockerName=dockerName,
		ports=ports,
		flags=flags,
		mount=mount,
		cmd=cmd,
		args=args,
		raw=argr,
		mac=mac,
		extra=extra
	).string()

def write_docker_compose(dockerName, ports=[], flags="", detatched=False, mount="/sync", dind=False, cmd="/bin/bash",name="kinde"):
	global docker

	try:
		from yaml import load, dump,safe_load
	except:
		os.system(str(sys.executable)+" -m pip install pyyaml")
		from yaml import load, dump, safe_load

	try:
		from yaml import CLoader as Loader, CDumper as Dumper
	except ImportError:
		from yaml import Loader, Dumper
	from fileinput import FileInput as finput

	print(os.path.exists("docker-compose.yml"))

	if os.path.exists("docker-compose.yml"):
		with open("docker-compose.yml", "r") as writer:
			contents = safe_load(writer)
	else:
		contents = {
			'services': {}
		}

	contents['services'][name] = {
		'image': dockerName,
		'privileged':dind,
		'volumes': [
			'./:'+str(mount)
		],
	}

	if dind:
		contents['services'][name]['volumes'] += ['/var/run/docker.sock:/var/run/docker.sock']

	portz = [x for x in getPort(ports,prefix="").split(' ') if x.strip() != '']
	if len(portz) >0:
		contents['services'][name]['ports'] = portz

	if cmd[0] is not None and cmd[0] != "/bin/bash":
		contents['services'][name]['command'] = cmd[0]

	with open("docker-compose.yml", "w+") as writer:
		dump(contents, writer, default_flow_style=False)

	return f"{docker} compose up " + str('-d' if detatched else '')

def update(url = "https://rebrand.ly/pydock"):
	try:
		import requests
	except:
		os.system(str(sys.executable) + " -m pip install requests")
		import requests

	try:
		new_contents = requests.get(url).text
		with open(__file__,'r+') as foil:
			data = foil.read()
			foil.seek(0)
			foil.write(new_contents)
			foil.truncate()
	except:
		pass

if __name__ == '__main__':
	if not os.path.exists('/usr/bin/docker') and not os.path.exists("/usr/local/bin/docker"):
		os.system("yes|apt-get install docker.io")

	sys_argz = ''.join(sys.argv)

	if "--short" in sys_argz:
		if "--short1" in sys_argz:
			sys.argv = "dock.sh -x run -d dev:lite --Login -p 5001 5000 --dind --savedir".split(" ")
		elif "--short2" in sys_argz:
			sys.argv = "dock.sh -x run -d dev:lite --Login -p 5001 5000 8888 8912 8899 --dind --savedir".split(" ")# + ["python -m pip install --upgrade pip xcyl hugg funbelts;/bin/cmd jupyterlab;/bin/cmd vs;/bin/cmd ipy;/bin/bash"]
		elif "--short3" in sys_argz:
			sys.argv = "dock.sh -x run -d dev:lite --Login -p 5001 5000 8912 8899 8888 6901 --dind --savedir".split(" ")
		elif "--shortvs" in sys_argz:
			sys.argv = "dock.sh -x run -d dev:lite --Login -p 8912 --dind --savedir".split(" ")
		elif "--shorty" in sys_argz:
			sys.argv = "dock.sh -x run -d dev:lite --Login --dind --savedir".split(" ")
		else:
			sys.argv = "dock.sh -x run -d pydev:lite --dind --savedir".split(" ")

	if "--vs" in sys_argz:
		sys.argv = """dock.sh -x run -d dev:ui --Login -p 5000 6901 --dind --savedir --raw "--shm-size=512m" --raw "-e" --raw "VNC_PW=password" --mountfrom :!""".split(" ") #docker run  --rm -it -v "`pwd`:/sync"   -p 6902:6901 --privileged --shm-size=512m -e VNC_PW=password  frantzme/dev:ui "/bin/bash echo "sudo apt-get install -y npm && sudo npm install -g npm@latest" >> /home/kasm-user/.bashrc && /bin/bash"

	if "--makerust" in sys_argz:
		rust_file = sys_argz.replace('dock.sh','').replace('--makerust','').strip()

		if "/dev/" in rust_file:
			splitr = None
			if "./" in rust_file:
				splitr = "./"
			elif "/sync/" in rust_file:
				splitr = "./"
			
			if splitr:
				rust_file = splitr + rust_file.split(splitr)[-1]

		sys.argv = "dock.sh -x run -d rustdev:lite -c /bin/single_run {0}".format(rust_file).split(" ")

	if "--grace" in sys_argz:
		sys.argv = """dock.sh -x run -d frantzme/ballerina:lite -p 8912 --dind --savedir --mountfrom :!""".split(" ")

	if "--graceExt" in sys_argz:
		sys.argv = """dock.sh -x run -d frantzme/ballerina:lite -p 8912 5000 --dind --savedir --mountfrom :!""".split(" ")

	if "--graceLogs" in sys_argz:
		sys.argv = """dock.sh -x graceLogs -d frantzme/ballerina:lite -p 8912 --dind --savedir --mountfrom :!""".split(" ")

	if '--shebang' in sys_argz:
		sys.argv = ' '.join(sys.argv[:-1]).split(' ')

	setGlobalArgs()
	args, cmds, execute = getArgs(), [], True

	regrun = lambda x:base_run(x, args.ports, "", args.mount, ' '.join(args.cmd),args, mac=args.mac, extra=''.join(args.extra), raw=args.raw)
	regcmd = lambda x,y:base_run(x, args.ports, "", args.mount, y,args, mac=args.mac, extra=''.join(args.extra), raw=args.raw)

	docker = "sudo docker" if use_sudo else "docker"

	if args.Login or args.Logg:
		cmds += [
			f"{docker} login"
		]

	for _cmd_string in args.command:
		_cmd_string = str(_cmd_string).strip().lower()

		if _cmd_string.strip() == "":
			print("No command specified")
			sys.exit(1)
		if _cmd_string == "update":
			update()
			sys.exit(1)
		if _cmd_string in ["clean","frun"]:
			cmds += dock().clean().split(";")
		if _cmd_string == "update":
			try:
				import requests
			except:
				os.system(str(sys.executable) + " -m pip install requests")
				import requests
			from fileinput import FileInput as finput

			resp = requests.get("https://rebrand.ly/pydock")
			if resp.ok:
				with finput(__file__,inplace=True) as foil:
					for old_line in foil:
						for line in resp.text.split('\n'):
							print(line)
						break
		if _cmd_string == "pose":
			#global baredocker
			write_docker_compose(sdock.docker.dock.dockerImage(args.docker[0],baredocker), args.ports, "", args.mount, args.cmd, args.name)
		if _cmd_string == "poser":
			#global baredocker
			cmds += [
				write_docker_compose(sdock.docker.dock.dockerImage(args.docker[0],baredocker), args.ports, "", args.mount, args.cmd,args.name),
				"rm docker-compose.yml"
			]
		if _cmd_string in ["run","frun"]:
			runningcmd = str(' '.join(args.cmd)).strip()
			#global baredocker
			cmds += [
				base_run(
					dockerName = sdock.docker.dock.dockerImage(args.docker[0],baredocker),
					ports = args.ports,
					cmd = None if runningcmd == '' else runningcmd,
					raw = args.raw,
					mount = args.mountfrom
				)
			]
		if _cmd_string == "wrap":
			cmds += [
				base_run(args.docker[0], args.ports, "", args.mount, args.cmd,args, mac=args.mac)
			]# + clean(args) #To Fix
		if _cmd_string == "pylite":
			cmds += [
				regrun("frantzme/pythondev:lite")
			]
		if _cmd_string == "writelite":
			cmds += [
				regrun("frantzme/writer:lite")
			]
		if _cmd_string == "jlite":
			cmds += [
				regrun("frantzme/javadev:lite")
			]
		if _cmd_string == "netdata" and False: #Need to figure out
			#global detach
			cmds += [
				base_run("netdata/netdata:latest", ['19999'], f"-v netdataconfig:/etc/netdata -v netdatalib:/var/lib/netdata -v netdatacache:/var/cache/netdata -v /etc/passwd:/host/etc/passwd:ro -v /etc/group:/host/etc/group:ro -v /proc:/host/proc:ro -v /sys:/host/sys:ro -v /etc/os-release:/host/etc/os-release:ro {'--restart unless-stopped' if detach else ''} --cap-add SYS_PTRACE --security-opt apparmor=unconfined", args.mount, "",args, mac=args.mac)
			]
		if _cmd_string == "mypy":
			cmds += [
				regcmd("frantzme/pythondev:latest", "bash -c \"cd /sync && ipython3 --no-banner --no-confirm-exit --quick\"")
			]
		if _cmd_string == "dive":
			#global baredocker
			#https://github.com/wagoodman/dive
			cmds += [
				f"{docker} pull {sdock.docker.dock.dockerImage(args.docker[0],args.baredocker)}",
				f"dive {sdock.docker.dock.dockerImage(args.docker[0],args.baredocker)}"
			]
		if _cmd_string == "build":
			cmds = [
				f"{docker} build -t {args.name[0]} .",
				f"{docker} run --rm -it -v \"{dir}:/sync\" {args.name[0]} {args.cmd}"
			]
		if _cmd_string == "lopy":
			cmds += [
				base_run("frantzme/pythondev:latest", [], "--env AUTHENTICATE_VIA_JUPYTER=\"password\"", args.mount, "bash -c \"cd /sync && ipython3 --no-banner --no-confirm-exit --quick -i {args.cmd} \"",args, mac=args.mac)
			]
		if _cmd_string == "blockly":
			cmds += [
				base_run("frantzme/ml:latest", ["5000"], "--env AUTHENTICATE_VIA_JUPYTER=\"password\"", args.mount, "blockly",args, mac=args.mac)
			]
		if _cmd_string == "mll":
			cmds += [
				base_run("dagshub/ml-workspace:latest", ["8080"], "--env AUTHENTICATE_VIA_JUPYTER=\"password\"", args.mount, "bash -c \"cd /sync && ipython3 --no-banner --no-confirm-exit --quick\"",args, mac=args.mac)
			]
		if _cmd_string == "labpy":
			cmds += [
				base_run("frantzme/pythondev:latest", ["8888"], "--env AUTHENTICATE_VIA_JUPYTER=\"password\"", args.mount, "jupyter lab --ip=0.0.0.0 --allow-root --port 8888 --notebook-dir=\"/sync/\"",args, mac=args.mac)
			]
		#sys.argv = """dock.sh -x graceLogs -d frantzme/ballerina:lite -p 8912 --dind --savedir --mountfrom :!""".split(" ")
		if False and _cmd_string == "graceLogs":
			#https://ballerina.io/learn/observe-metrics/
			cmds += [
				base_run("frantzme/pythondev:latest", ["8888"], "--env AUTHENTICATE_VIA_JUPYTER=\"password\"", args.mount, "jupyter lab --ip=0.0.0.0 --allow-root --port 8888 --notebook-dir=\"/sync/\"",args, mac=args.mac)
			]
		if _cmd_string == "jlab":
			cmds += [
				base_run("oneoffcoder/java-jupyter", ["8675"], None,None, args.mount, f"jupyter lab --ip=0.0.0.0 --allow-root --port 8675 --notebook-dir=\"/sync/\"",args, mac=args.mac)
			]
		if _cmd_string == "gclone": #dock.sh -x frun -d alpine/git:latest --baredocker -c clone https://github.com/franceme/franceme.github.io /sync/franceme.github.io
			for arg in args.cmd:
				cmds += [
					base_run("alpine/git:latest", args.ports, None,None, args.mount, f"clone {arg} {args.mount}/{arg.split('/')[-1]}",args,baredocker=False, mac=args.mac)
				]
		if _cmd_string == "lab":
			cmds += [
				base_run("frantzme/pythondev:latest", ["8675"], None, None, args.mount, f"jupyter lab --ip=0.0.0.0 --allow-root --port 8675 --notebook-dir=\"/sync/\"",args, mac=args.mac)
			]
		if _cmd_string == "sos":
			cmds += [
				base_run("vatlab/sos-notebook", ["8678"], None, None, "/home/jovyan/work", f"jupyter lab --ip=0.0.0.0 --allow-root --port 8678",args, mac=args.mac)
			]
		if _cmd_string == "polynote":
			#https://github.com/polynote/polynote/blob/master/docker/README.md
			cmds += [
				base_run("polynote/polynote:latest", ["8192"], None, None, "data", f"-p 127.0.0.1:8192:8192 -p 127.0.0.1:4040-4050:4040-4050",args, mac=args.mac)
			]
		if _cmd_string == "polynote2":
			cmds += [
				base_run("xtreamsrl/polynote-docker", ["8192"],None, "/data", args.cmd,args, mac=args.mac)
			]
		if _cmd_string == "cmd":
			cmds += [
				base_run(args.docker[0], args.ports, None, None, args.mount, ' '.join(args.cmd),args, mac=args.mac)
			]
		if _cmd_string == "qodana-jvm":
			output_results = "qodana_jvm_results"
			try:
				os.system(f"mkdir {output_results}")
			except:
				pass

			cmds += [
				base_run("jetbrains/qodana-jvm", ["8080"], f"-v \"{output_results}:/data/results/\"  --show-report", "/data/project/", args.mount, "/bin/bash",args, mac=args.mac)
			]
		if _cmd_string == "qodana-py":
			cmds += [
				base_run("jetbrains/qodana-python:2022.1-eap", ["8080"], "--show-report", "/data/project/", args.mount, "/bin/bash",args, mac=args.mac)
			]
		if _cmd_string == "splunk":
			cmds += [
				base_run("splunk/splunk:latest", ["8000"], "-e SPLUNK_START_ARGS='--accept-license' -e SPLUNK_PASSWORD='password'",None, args.mount, "start",args, mac=args.mac)
			]
		if _cmd_string == "beaker":
			cmds += [
				base_run("beakerx/beakerx", ["8888"], None, args.mount, "/bin/bash",args, mac=args.mac)
			]
		if _cmd_string == "superset":
			cmds += [
				base_run("apache/superset:latest", ["8088"], None, args.mount, "/bin/bash",args, mac=args.mac)
			]
		if _cmd_string == "mysql":
			cmds += [
				base_run("mysql:latest", ["3306"], "-e MYSQL_ROOT_PASSWORD=root", args.mount, "/bin/bash",args, mac=args.mac)
			]
		if _cmd_string in ["load","pull"]:
			#global baredocker
			cmds += [
				f"{docker} pull {sdock.docker.dock.dockerImage(args.docker[0],baredocker)}"
			]
		if _cmd_string in ["clean","frun"]:
			cmds += dock().clean().split(";")
		if _cmd_string == "stop":
			cmds += [f"{docker} kill $({docker} ps -a -q)"]
		if _cmd_string == "list":
			cmds += [f"{docker} images"]
		if _cmd_string == "live":
			cmds += [f"{docker} ps|awk '{{print $1, $3}}'"]
		if _cmd_string == "update":
			containerID = run(f"{docker} ps |awk '{{print $1}}'|tail -1")
			imageID = run(f"{docker} ps |awk '{{print $2}}'|tail -1")

			cmds += [
				f"{docker} commit {containerID} {imageID}",
				f"{docker} push {imageID}"
			]
		if _cmd_string == "kill":
			base_dock(args.docker[0]).kill()
		if _cmd_string in ["loads","pulls"]:
			for load in args.docker:
				#global baredocker
				cmds += [f"{docker} pull {sdock.docker.dock.dockerImage(load,baredocker)}"]

		if args.Logout or args.Logg:
			cmds += [
				f"{docker} logout"
			]

	cmds = flatten_list(cmds)
	print(cmds)
	for x in cmds:
		try:
			print(f"> {x}")
			if args.execute:
				try:
					os.system(x)
				except: pass
		except:
			pass
