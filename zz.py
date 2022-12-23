#!/usr/bin/env python3
'''####################################
#Version: 00.00
#Version Numbering: Major.Minor
#Reasons for imports
		os							  : used for verifying and reading files
		sys					 : used for exiting the system
'''####################################

##Imports
import os
import sys
import subprocess
import platform
import socket

try:
	import sdock
except:
	os.system("{0} -m pip install --upgrade sdock".format(sys.executable))
	import sdock

'''####################################
#The main runner of this file, intended to be ran from
'''####################################

computers = {
	"=":{},
	"self":{
			"user":os.path.expanduser('~').split('/')[-1],
			"ip":"127.0.0.1",
			"port":22,
			"sudo":False,
	}
}

def dir_of(path):
	return os.path.abspath(path)

cur_dir = lambda:dir_of(os.curdir)

remote_file = lambda remote,file:  file.strip().replace('__/','/home/' + remote['user'] + '/Downloads/').replace('_/', '/home/' + remote['user'] + '/').strip()

def getArgs():
	import argparse
	parser = argparse.ArgumentParser("ZZ aide")
	parser.add_argument("-n","--name", help="The name of the endpoint", nargs=1, default="remote")
	parser.add_argument("-f","--foil", help="The location file of additional computers", nargs='?', default=None)
	parser.add_argument("-p","--ports", help="The ports to be exposed", nargs="*", default=[])
	parser.add_argument("-c","--cmd", help="The cmd to be run", nargs="*", default=[])
	parser.add_argument("--ssh", help="Change the ssh port", nargs="?", default=None)
	parser.add_argument("--upload",help="Upload the file", nargs="?", default=None)
	parser.add_argument("--download",help="Download the file", nargs="?", default=None)
	parser.add_argument("--sdel", help="Delete the file (only for the upload/download)",action='store_true',default=False)
	parser.add_argument("--sudo", help="Prefix Sudo to the commands",action='store_true',default=False)
	parser.add_argument("--jupyter", help="Run JupyterLab",action='store_true',default=False)
	parser.add_argument("--splunk", help="Run Splunk",action='store_true',default=False)
	parser.add_argument("--sdock", help="Run Docker as Sudo",action="store_true",default=False)
	parser.add_argument("--vagrant", help="Run Vagrant",action='store_true',default=False)
	parser.add_argument("--pycharm", help="Run PyCharm",nargs="?", default=None)
	parser.add_argument("--datagrip", help="Run DataGrip",nargs="?", default=None)
	parser.add_argument("--intellij", help="Run Intellij",nargs="?", default=None)
	parser.add_argument("--pyqodana", help="Run PyQodana",nargs="?", default=None)
	parser.add_argument("--jqodana", help="Run Java Qodana",nargs="?", default=None)
	parser.add_argument("--reverse", help="Create a Dockerfile from the Image",nargs="?", default=None)
	parser.add_argument("--blender", help="Run Blender",action='store_true',default=False)
	#https://docs.firefly-iii.org/firefly-iii/installation/docker/
	parser.add_argument("--firefly", help="Run Firefly 3",action='store_true',default=False)
	parser.add_argument("--hoppscotch", help="Run HoppScotch",action='store_true',default=False)
	parser.add_argument("--postman", help="Run HoppScotch (alias for postman)",action='store_true',default=False)
	parser.add_argument("--results", help="Any Results Directory",nargs="?", default="RunResults")
	return parser.parse_args()

def run(remote,cmd='',port=''):
	run_cmd = 'sudo su' if remote['sudo'] else ''
	if cmd.strip() != '':
		run_cmd = cmd
	#return f"ssh -t {remote['port']} {port} {remote['user']}@{remote['ip']} {run_cmd}"
	if remote['ip'] != '127.0.0.1':
		return f"ssh -t {port} {remote['user']}@{remote['ip']} {run_cmd}"
	else:
		return run_cmd


def down(remote,file):
	#return f"scp -t {remote['port']} {remote['user']}@{remote['ip']}:{file} ./"
	return f"scp {remote['user']}@{remote['ip']}:{remote_file(remote,file)} ./"

def up(remote,file):
	#return f"scp -t {remote['port']} {file.strip()} {remote['user']}@{remote['ip']}:/tmp/"
	return f"scp {file.strip()} {remote['user']}@{remote['ip']}:/tmp/"

if __name__ == '__main__':
	args = getArgs()

	prefix = ""
	if args.sudo:
		prefix += " sudo "
	
	if args.foil and os.path.exists(args.foil):
		import json
		with open(args.foil,'r') as reader:
			computers = {**computers, **json.load(reader)}

	working_computers,cmds = [],[]

	if args.name[0] == "=":
		working_computers = [value for key,value in computers.items() if key != "=" and key != "self"]
	else:
		working_computers = [computers[args.name[0]]]

	#sdock = "sudo docker" if args.sdock else "docker"

	for computer in working_computers:
		if args.ssh is not None:
			computer['port'] = args.ssh

		bare_run = True

		if args.jupyter:
			cmds += [" jupyter lab --allow-root"]
			args.ports += ["8888"]
			bare_run &= False
		elif args.splunk:
			#cmds += [prefix + f" docker run -p 8000:8000 -v /home/{computer['user']}:/sync -e SPLUNK_START_ARGS='--accept-license' -e SPLUNK_PASSWORD='password' splunk/splunk:latest"]
			#args.ports += ["8000"]
			cmds += [
				sdock.sdock(
					docker = "docker",
					image = "splunk/splunk:latest",
					ports = [8000],
					cmd = None,
					dind = False,
					shared = False,
					detach = False,
					sudo = False,
					remove = True,
					mountto = "/sync",
					mountfrom = f"/home/{computer['user']}",
					#name: str = "current_running"
					login = False,
					loggout = False,
					logg = False,
					macaddress = None,
					postClean = False,
					preClean = False,
					extra = "-e SPLUNK_START_ARGS='--accept-license' -e SPLUNK_PASSWORD='password'"
				)
			]
			bare_run &= False
		elif args.blender:
			#cmds += [prefix + f" docker run -p 3000:3000 -v /home/{computer['user']}:/sync linuxserver/blender:latest"]
			#args.ports += ["3000"]
			cmds += [
				sdock.sdock(
					docker = "docker",
					image = "linuxserver/blender:latest",
					ports = [3000],
					cmd = None,
					dind = False,
					shared = False,
					detach = False,
					sudo = False,
					remove = True,
					mountto = "/sync",
					mountfrom = f"/home/{computer['user']}",
					#name: str = "current_running"
					login = False,
					loggout = False,
					logg = False,
					macaddress = None,
					postClean = False,
					preClean = False,
					extra = None
				).string()
			]
			bare_run &= False
		elif args.firefly:
			#cmds += [prefix + f" docker run -p 8080:8080 -e APP_KEY=CHANGEME_32_CHARS -e DB_HOST=CHANGEME -e DB_PORT=3306 -e DB_CONNECTION=mysql -e DB_DATABASE=CHANGEME -e DB_USERNAME=CHANGEME -e DB_PASSWORD=CHANGEME -v /home/{computer['user']}:/var/www/html/storage/upload fireflyiii/core:latest"]
			#args.ports += ["8080"]
			cmds += [
				sdock.sdock(
					docker = "docker",
					image = "fireflyiii/core:latest",
					ports = [8080],
					cmd = None,
					dind = False,
					shared = False,
					detach = False,
					sudo = False,
					remove = True,
					mountto = "/var/www/html/storage/upload",
					mountfrom = f"/home/{computer['user']}",
					#name: str = "current_running"
					login = False,
					loggout = False,
					logg = False,
					macaddress = None,
					postClean = False,
					preClean = False,
					extra = "-e APP_KEY=CHANGEME_32_CHARS -e DB_HOST=CHANGEME -e DB_PORT=3306 -e DB_CONNECTION=mysql -e DB_DATABASE=CHANGEME -e DB_USERNAME=CHANGEME -e DB_PASSWORD=CHANGEME"
				).string()
			]
			bare_run &= False
		elif args.hoppscotch or args.postman:
			#cmds += [prefix + f" docker run -p 3000:3000 -v /home/{computer['user']}:/sync hoppscotch/hoppscotch:latest"]
			#cmds += [prefix + f" docker run --shm-size=512m -p 6901:6901 -v /home/{computer['user']}:/sync -e VNC_PW=password kasmweb/insomnia:1.12.0"]
			#args.ports += ["3000"]
			cmds += [
				sdock.sdock(
					docker = "docker",
					image = "kasmweb/insomnia:1.12.0",
					ports = [6901],
					cmd = None,
					dind = False,
					shared = False,
					detach = False,
					sudo = False,
					remove = True,
					mountto = "/sync",
					mountfrom = f"/home/{computer['user']}",
					#name: str = "current_running"
					login = False,
					loggout = False,
					logg = False,
					macaddress = None,
					postClean = False,
					preClean = False,
					extra = "--shm-size=512m -e VNC_PW=password"
				).string()
			]
			bare_run &= False
		elif False: #args.blender:https://hub.docker.com/u/linuxserver
			#cmds += [prefix + f" docker run -p 3000:3000 -v /home/{computer['user']}:/sync linuxserver/blender"]
			#args.ports += ["3000"] 
			bare_run &= False
			sys.exit(0)
		elif args.reverse:
			#cmds += [prefix + f" docker pull {args.reverse} && {prefix} docker run --privileged=true -v /var/run/docker.sock:/var/run/docker.sock --rm ghcr.io/laniksj/dfimage {args.reverse}"]
			cmds += [f"docker pull {args.reverse} && " + 
				sdock.sdock(
					docker = "docker",
					image = "ghcr.io/laniksj/dfimage",
					ports = [6901],
					cmd = None,
					dind = True,
					shared = False,
					detach = False,
					sudo = False,
					remove = True,
					mountto = "/sync",
					mountfrom = f"/home/{computer['user']}",
					#name: str = "current_running"
					login = False,
					loggout = False,
					logg = False,
					macaddress = None,
					postClean = False,
					preClean = False,
					extra = args.reverse
				).string()
			]
			bare_run &= False
		elif args.vagrant:
			print("Vagrant is not currently Setup and Ran")
			bare_run &= False
			sys.exit(0)
			#cmds += [prefix + "apt-get install virtual-box vagrant"]
			#args.ports += ["8000"]
		elif args.pyqodana:
			#https://www.jetbrains.com/help/qodana/qodana-python-docker-readme.html#b920fd1
			args.pyqodana = os.path.abspath(args.pyqodana)
			path = '/'.join(args.pyqodana.split('/')[:-1])

			args.results = os.path.join(path, args.results)
			try:
				watch_cmd(f"yes|rm -r {args.results}/")
			except:
				pass
			#cmds += [f" {sdock} run --rm -it -v {args.pyqodana}/:/data/project/ -v {args.results}/:/data/results/ jetbrains/qodana-python && mv {args.results} {args.pyqodana}"]
			cmds += [
				sdock.sdock(
					docker = "docker",
					image = "jetbrains/qodana-python",
					ports = [6901],
					cmd = None,
					dind = True,
					shared = False,
					detach = False,
					sudo = False,
					remove = True,
					mountto = "/data/project/",
					mountfrom = args.pyqodana,
					#name: str = "current_running"
					login = False,
					loggout = False,
					logg = False,
					macaddress = None,
					postClean = False,
					preClean = False,
					extra = f"-v {args.results}/:/data/results/"
				).string() + f"&& mv {args.results} {args.pyqodana}"
			]
			bare_run &= False
		elif args.jqodana:
			#https://www.jetbrains.com/help/qodana/qodana-jvm-community-docker-readme.html#quick-start-recommended-profile
			args.jqodana = os.path.abspath(args.jqodana)
			path = '/'.join(args.jqodana.split('/')[:-1])

			args.results = os.path.join(path, args.results)
			try:
				watch_cmd(f"yes|rm -r {args.results}/")
			except:
				pass
			#cmds += [f" {sdock} run --rm -it -v {args.jqodana}/:/data/project/ -v {args.results}/:/data/results/ jetbrains/qodana-jvm-community && mv {args.results} {args.jqodana}"]
			cmds += [
				sdock.sdock(
					docker = "docker",
					image = "jetbrains/qodana-jvm-community",
					ports = [6901],
					cmd = None,
					dind = True,
					shared = False,
					detach = False,
					sudo = False,
					remove = True,
					mountto = "/data/project/",
					mountfrom = args.jqodana,
					#name: str = "current_running"
					login = False,
					loggout = False,
					logg = False,
					macaddress = None,
					postClean = False,
					preClean = False,
					extra = f"-v {args.results}/:/data/results/"
				).string() + f"&& mv {args.results} {args.jqodana}"
			]
			bare_run &= False
		elif args.pycharm:
			#https://stackoverflow.com/questions/28717464/docker-expose-all-ports-or-range-of-ports-from-7000-to-8000
			#args.cmd = f"docker run --rm -it --privileged=true -v /var/run/docker.sock:/var/run/docker.sock -v {os.path.abspath(args.pycharm)}/:/project -p {try_port('8887')}:8887 registry.jetbrains.team/p/prj/containers/projector-pycharm-p".split()
			#cmds += [f" {sdock} run --rm -it --privileged=true -v /var/run/docker.sock:/var/run/docker.sock -v {os.path.abspath(args.pycharm)}/:/project -p {try_port('8887')}:8887  -p 3000-4000:3000-4000 frantzme/pycharm:latest"]
			cmds += [
				sdock.sdock(
					docker = "docker",
					image = "frantzme/pycharm:latest",
					ports = [8887],
					cmd = None,
					dind = True,
					shared = False,
					detach = False,
					sudo = False,
					remove = True,
					mountto = "/project/",
					mountfrom = os.path.abspath(args.pycharm),
					#name: str = "current_running"
					login = False,
					loggout = False,
					logg = False,
					macaddress = None,
					postClean = False,
					preClean = False,
					extra = None
				).string()
			]
			bare_run &= False
		elif args.intellij:
			#args.cmd = f"sudo docker run --rm -it --privileged=true -v /var/run/docker.sock:/var/run/docker.sock -v {os.path.abspath(args.intellij)}/:/project -p {try_port('8887')}:8887 registry.jetbrains.team/p/prj/containers/projector-idea-u".split()
			#cmds += [f" {sdock} run --rm -it --privileged=true -v /var/run/docker.sock:/var/run/docker.sock -v {os.path.abspath(args.intellij)}/:/project -p {try_port('8887')}:8887  -p 3000-4000:3000-4000 frantzme/intellij:latest"]
			cmds += [
				sdock.sdock(
					docker = "docker",
					image = "frantzme/pycharm:latest",
					ports = [8887],
					cmd = None,
					dind = True,
					shared = False,
					detach = False,
					sudo = False,
					remove = True,
					mountto = "/project/",
					mountfrom = os.path.abspath(args.intellij),
					#name: str = "current_running"
					login = False,
					loggout = False,
					logg = False,
					macaddress = None,
					postClean = False,
					preClean = False,
					extra = None
				).string()
			]
			bare_run &= False

		elif args.datagrip:
			#args.cmd = f"sudo docker run --rm -it --privileged=true -v /var/run/docker.sock:/var/run/docker.sock -v {os.path.abspath(args.intellij)}/:/project -p {try_port('8887')}:8887 registry.jetbrains.team/p/prj/containers/projector-idea-u".split()
			#cmds += [f" {sdock} run --rm -it --privileged=true -v /var/run/docker.sock:/var/run/docker.sock -v {os.path.abspath(args.datagrip)}/:/project -p {try_port('8887')}:8887  -p 3000-4000:3000-4000 frantzme/mygrip:latest"]
			cmds += [
				sdock.sdock(
					docker = "docker",
					image = "frantzme/pycharm:latest",
					ports = [8887],
					cmd = None,
					dind = True,
					shared = False,
					detach = False,
					sudo = False,
					remove = True,
					mountto = "/project/",
					mountfrom = os.path.abspath(args.datagrip),
					#name: str = "current_running"
					login = False,
					loggout = False,
					logg = False,
					macaddress = None,
					postClean = False,
					preClean = False,
					extra = None
				).string()
			]
			bare_run &= False
		print(bare_run)


		if args.download:
			cmds += [down(computer, args.download)]
			if args.sdel:
				cmds += [
					run(computer,f" \" yes|rm {remote_file(computer,args.download)} \"").replace('-t','')
				]
			bare_run &= False
		elif args.upload:
			cmds += [up(computer, args.upload)]
			if args.sdel:
				cmds += [
					f"yes|rm {args.upload}"
				]
			bare_run &= False
		else:
			print("HIT")
			ports = ""
			for port in set(args.ports):
				ports += f" -L {sdock.getPort(port)}:{computer['ip']}:{port} "

			cmds += [run(computer,' '.join(args.cmd), ports)]
		
	print(cmds)
	for x in cmds:
		print(x);os.system(x)
