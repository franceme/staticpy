#!/usr/bin/env python3
'''####################################
#Version: 00.00
#Version Numbering: Major.Minor
#Reasons for imports
		os							  : used for verifying and reading files
		sys					 : used for exiting the system
python3 <(curl -sL https://rebrand.ly/pyzz)
'''####################################

##Imports
import os
import sys
import subprocess
import platform
import socket
import sdock
from sdock.docker import dock

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
# Global Arguments
network = None
use_sudo = False
dind = False
detach = False
savedir = False
baredocker = None

def getArgs():
	import argparse
	parser = argparse.ArgumentParser("ZZ aide")
	parser.add_argument("-n","--name", help="The name of the endpoint", nargs=1, default="self")
	parser.add_argument("-f","--foil", help="The location file of additional computers", nargs='?', default=None)
	parser.add_argument("-p","--ports", help="The ports to be exposed", nargs="*", default=[])
	parser.add_argument("-c","--cmd", help="The cmd to be run", nargs="*", default=[])
	parser.add_argument("--print", help="Only print the docker command",action='store_true',default=False)
	parser.add_argument("--ssh", help="Change the ssh port", nargs="?", default=None)
	parser.add_argument("--upload",help="Upload the file", nargs="?", default=None)
	parser.add_argument("--download",help="Download the file", nargs="?", default=None)
	parser.add_argument("--sdel", help="Delete the file (only for the upload/download)",action='store_true',default=False)
	parser.add_argument("--sudo", help="Prefix Sudo to the commands",action='store_true',default=False)
	parser.add_argument("--jupyter", help="Run JupyterLab",action='store_true',default=False)
	parser.add_argument("--splunk", help="Run Splunk",nargs="?", default=None)
	parser.add_argument("--sdock", help="Run Docker as Sudo",action="store_true",default=False)
	parser.add_argument("--vagrant", help="Run Vagrant",action='store_true',default=False)
	parser.add_argument("--dockerSwarm", help="Run DockerSwarm",action='store_true',default=False)
	parser.add_argument("--pycharm", help="Run PyCharm",nargs="?", default=None)
	parser.add_argument("--office", help="Run the libreoffice app",nargs="?", default=None)
	parser.add_argument("--runme", help="Run the RunMe docker image",nargs="?", default=None)
	parser.add_argument("--webstorm", help="Run WebStorm",nargs="?", default=None)
	parser.add_argument("--swaggergenpy", help="Generate a Python Swaggerhub ClientSDK From swagger.json file",nargs="?", default=None)
	parser.add_argument("--datagrip", help="Run DataGrip",nargs="?", default=None)
	parser.add_argument("--grist", help="Run Grist",nargs="?", default=None)
	parser.add_argument("--dejs", help="Run the JavaScript deobfuscator",nargs="?", default=None)
	parser.add_argument("--intellij", help="Run Intellij",nargs="?", default=None)
	parser.add_argument("--pyqodana", help="Run PyQodana",nargs="?", default=None)
	parser.add_argument("--jqodana", help="Run Java Qodana",nargs="?", default=None)
	parser.add_argument("--reverse", help="Create a Dockerfile from the Image",nargs="?", default=None)
	parser.add_argument("--blender", help="Run Blender",action='store_true',default=False)
	#https://docs.firefly-iii.org/firefly-iii/installation/docker/
	parser.add_argument("--redirect", help="Run a Redirect Service",action='store_true',default=False)
	parser.add_argument("--firefly", help="Run Firefly 3",action='store_true',default=False)
	parser.add_argument("--hoppscotch", help="Run HoppScotch",action='store_true',default=False)
	parser.add_argument("--zoom", help="Run Zoom",action='store_true',default=False)
	#parser.add_argument("--knime", help="Run Knime",action='store_true',default=False)
	parser.add_argument("--mrust", help="Run a mini Rust Docker container",nargs="?", default=None)
	parser.add_argument("--postman", help="Run HoppScotch (alias for postman)",action='store_true',default=False)
	parser.add_argument("--dozzle", help="Run Dozzle (monitor of docker images)",action='store_true',default=False)
	parser.add_argument("--inkscape", help="Run inkscape",action='store_true',default=False)
	parser.add_argument("--ui", help="Run the base ui base docker image",nargs="?", default=None)
	parser.add_argument("--knime", help="Run the base knime docker image",nargs="?", default=None)
	parser.add_argument("--ref", help="Run the ref base docker image",nargs="?", default=None)
	parser.add_argument("--gsync", help="Run the base gsync base docker image",nargs="?", default=None)
	parser.add_argument("--tor", help="Run TorBrowser",action='store_true',default=False)
	parser.add_argument("--dbhub", help="Run a local instance of DBHub",action='store_true',default=False)
	parser.add_argument("--colab", help="Run a local instance for Google Colab",action='store_true',default=False)
	parser.add_argument("--results", help="Any Results Directory",nargs="?", default="RunResults")
	parser.add_argument("--ball", help="Run Ballerina with folder",nargs="?", default=None)
	parser.add_argument("--openrefine", help="Run the openrefine app",nargs="?", default=None)
	parser.add_argument("--superset", help="Run the superset app",nargs="?", default=None)
	parser.add_argument("--gridstore", help="Prefix gridstore app",action='store_true',default=False)
	parser.add_argument("--elyra", help="Prefix elyra app",action='store_true',default=False)
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
	parser.add_argument("--baredocker", help="Don't use the bare docker name provided", action="store_true",default=False)

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
	setGlobalArgs()
	args = getArgs()
	# global network
	# global use_sudo
	# global dind
	# global detach
	# global savedir
	# global baredocker

	sudo = args.sudo or use_sudo

	prefix = ""
	if sudo:
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
				dock(save_host_dir=savedir,network = network,
					docker = "docker",
					image = "splunk/splunk:latest",
					ports = [8000, 8088],
					cmd = "start",
					#nocmd = True,
					dind = dind,
					shared = False,
					detach = detach,
					sudo = sudo,
					remove = True,
					mountto = "/sync",
					mountfrom = args.splunk,
					#name: str = "current_running"
					login = False,
					loggout = False,
					logg = False,
					macaddress = None,
					postClean = False,
					preClean = False,
					extra = "-e SPLUNK_START_ARGS='--accept-license' -e SPLUNK_PASSWORD='password'"
				).string()
			]
			bare_run &= False
		elif args.colab:
			#docker run -p 127.0.0.1:9000:8080 us-docker.pkg.dev/colab-images/public/runtime
			#https://research.google.com/colaboratory/local-runtimes.html
			cmds += [
				dock(save_host_dir=savedir,network = network,
					docker = "docker",
					image = "us-docker.pkg.dev/colab-images/public/runtime",
					ports = [9000],
					#ports = [9000:8080],
					cmd = None,
					#nocmd = True,
					dind = dind,
					shared = False,
					detach = detach,
					sudo = sudo,
					remove = True,
					mountto = None,
					mountfrom = None,
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
		elif args.blender:
			#cmds += [prefix + f" docker run -p 3000:3000 -v /home/{computer['user']}:/sync linuxserver/blender:latest"]
			#args.ports += ["3000"]
			if False:
				cmds += [
					dock(save_host_dir=savedir,network = network,
						docker = "docker",
						image = "linuxserver/blender:latest",
						ports = [3000],
						cmd = None,
						#nocmd = True,
						dind = dind,
						shared = False,
						detach = detach,
						sudo = sudo,
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
		elif args.openrefine:
			#https://hub.docker.com/r/felixlohmeier/openrefine/
			#cmds += [prefix + f" docker run -p 3000:3000 -v /home/{computer['user']}:/sync linuxserver/blender:latest"]
			#cmds += [docker run --rm -p 80:3333 -v /home/felix/refine:/data:z felixlohmeier/openrefine:3.5.0 -i 0.0.0.0 -d /data -m 4G]
			if True:
				cmds += [
					dock(save_host_dir=savedir,network = network,
						docker = "docker",
						image = "felixlohmeier/openrefine:3.5.0",
						ports = [3333],
						cmd = None,
						#nocmd = True,
						dind = dind,
						shared = False,
						detach = detach,
						sudo = sudo,
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
						extra = "-d /data -m 4G"
					).string()
				]
		elif args.gridstore:
			#https://github.com/ricklamers/gridstudio
			#args.ports += ["3000"]
			if True:
				cmds += [
					"wget https://github.com/ricklamers/gridstudio/archive/refs/heads/master.zip",
					"7z x master.zip",
					"rm master.zip",
					"cd gridstudio-master/ && chmod 777 run.sh && ./run.sh",
					"yes|rm -r gridstudio-master/",
				]
		elif args.elyra:
			#https://github.com/elyra-ai/elyra
			#cmds += [docker run -it -p 8888:8888 -v ${HOME}/opensource/jupyter-notebooks/:/home/jovyan/work -w /home/jovyan/work elyra/elyra:dev jupyter lab --debug]
			#args.ports += ["3000"]
			## https://files.pythonhosted.org/packages/f0/3a/f5ce74b2bdbbe59c925bb3398ec0781b66a64b8a23e2f6adc7ab9f1005d9/apache_airflow-1.10.15-py2.py3-none-any.whl
			## Added medium assist https://medium.com/ibm-data-ai/getting-started-with-apache-airflow-operators-in-elyra-aae882f80c4a
			cmds += [
				dock(save_host_dir=savedir,network = network,
					docker = "docker",
					image = "elyra/elyra",
					ports = [8888],
					cmd = None,
					#nocmd = True,
					dind = dind,
					shared = False,
					detach = detach,
					sudo = sudo,
					remove = True,
					mountto = "/sync", #"/home/jovyan/work",
					mountfrom = f"/home/{computer['user']}",
					name = "superset",
					login = False,
					loggout = False,
					logg = False,
					macaddress = None,
					postClean = False,
					preClean = False,
					extra = """-w /sync """
				).string()
			]
		elif args.superset:
			#https://hub.docker.com/r/apache/superset
			#cmds += [docker run -d -p 8080:8088 -e "SUPERSET_SECRET_KEY=your_secret_key_here" --name superset apache/superset]
			#args.ports += ["3000"]
			if True:
				cmds += [
					dock(save_host_dir=savedir,network = network,
						docker = "docker",
						image = "apache/superset",
						ports = [8080],
						cmd = None,
						#nocmd = True,
						dind = dind,
						shared = False,
						detach = detach,
						sudo = sudo,
						remove = True,
						mountto = "/sync",
						mountfrom = f"/home/{computer['user']}",
						name = "superset",
						login = False,
						loggout = False,
						logg = False,
						macaddress = None,
						postClean = False,
						preClean = False,
						extra = """-e "SUPERSET_SECRET_KEY=REALLYREALLYREALLYSECRETKEYH3R3" """
					).string(),
					"""docker exec -it superset superset fab create-admin --username admin --firstname Superset --lastname Admin --email admin@superset.com --password admin""",
					"""docker exec -it superset superset db upgrade""",
					"""docker exec -it superset superset load_examples""",
					"""docker exec -it superset superset init"""
				]
			else:
				cmds += [
					dock(save_host_dir=savedir,network = network,
						docker = "docker",
						image = "kasmweb/blender:1.12.0",
						ports = [6901],
						cmd = None,
						#nocmd = True,
						dind = dind,
						shared = False,
						detach = detach,
						sudo = sudo,
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
		elif args.tor:
			cmds += [
				dock(save_host_dir=savedir,network = network,
					docker = "docker",
					image = "kasmweb/tor-browser:1.12.0",
					ports = [6901],
					cmd = None,
					#nocmd = True,
					dind = dind,
					shared = False,
					detach = detach,
					sudo = sudo,
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
		elif args.firefly:
			#cmds += [prefix + f" docker run -p 8080:8080 -e APP_KEY=CHANGEME_32_CHARS -e DB_HOST=CHANGEME -e DB_PORT=3306 -e DB_CONNECTION=mysql -e DB_DATABASE=CHANGEME -e DB_USERNAME=CHANGEME -e DB_PASSWORD=CHANGEME -v /home/{computer['user']}:/var/www/html/storage/upload fireflyiii/core:latest"]
			#args.ports += ["8080"]
			cmds += [
				dock(save_host_dir=savedir,network = network,
					docker = "docker",
					image = "fireflyiii/core:latest",
					ports = [8080],
					cmd = None,
					#nocmd = True,
					dind = dind,
					shared = False,
					detach = detach,
					sudo = sudo,
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
		elif args.dbhub: #https://hub.docker.com/r/sqlitebrowser/dbhub.io-dev
			cmds += [
				dock(save_host_dir=savedir,network = network,
					docker = "docker",
					image = "sqlitebrowser/dbhub.io-dev:latest",
					ports = [5550,9000,8443],
					cmd = None,#"/usr/local/bin/init.sh;/usr/local/bin/start.sh",
					#nocmd = True,
					dind = dind,
					shared = False,
					detach = detach,
					sudo = sudo,
					remove = True,
					mountto = None, #"/data",
					mountfrom = None, #os.path.abspath(args.dbhub),
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
		elif args.hoppscotch or args.postman:
			#cmds += [prefix + f" docker run -p 3000:3000 -v /home/{computer['user']}:/sync hoppscotch/hoppscotch:latest"]
			#cmds += [prefix + f" docker run --shm-size=512m -p 6901:6901 -v /home/{computer['user']}:/sync -e VNC_PW=password kasmweb/insomnia:1.12.0"]
			#args.ports += ["3000"]
			cmds += [
				dock(save_host_dir=savedir,network = network,
					docker = "docker",
					image = "kasmweb/insomnia:1.12.0",
					ports = [6901],
					cmd = None,
					#nocmd = True,
					dind = dind,
					shared = False,
					detach = detach,
					sudo = sudo,
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
		elif args.zoom:
			#cmds += [prefix + f" docker run -p 3000:3000 -v /home/{computer['user']}:/sync hoppscotch/hoppscotch:latest"]
			#cmds += [prefix + f" docker run --shm-size=512m -p 6901:6901 -v /home/{computer['user']}:/sync -e VNC_PW=password kasmweb/insomnia:1.12.0"]
			#args.ports += ["3000"]
			cmds += [
				dock(save_host_dir=savedir,network = network,
					docker = "docker",
					image = "frantzme/dev:zoom",
					ports = [6901],
					cmd = None,
					#nocmd = True,
					dind = dind,
					shared = False,
					detach = detach,
					sudo = sudo,
					remove = True,
					#mountto = "/sync",
					#mountfrom = f"/home/{computer['user']}",
					#name: str = "current_running"
					login = True,
					loggout = True,
					logg = False,
					macaddress = None,
					postClean = False,
					preClean = False,
					extra = "--shm-size=512m -e VNC_PW=password"
				).string()
			]
			bare_run &= False
		elif args.dozzle:
			#https://github.com/amir20/dozzle
			#cmds += [prefix + f" docker run -p 3000:3000 -v /home/{computer['user']}:/sync hoppscotch/hoppscotch:latest"]
			#cmds += [prefix + f" docker run --shm-size=512m -p 6901:6901 -v /home/{computer['user']}:/sync -e VNC_PW=password kasmweb/insomnia:1.12.0"]
			#args.ports += ["3000"]
			cmds += [
				dock(save_host_dir=savedir,network = network,
					docker = "docker",
					image = "amir20/dozzle:latest",
					ports = [8080],
					cmd = None,
					#nocmd = True,
					dind = False,
					shared = False,
					detach = detach,
					sudo = sudo,
					remove = True,
					#mountto = "/sync",
					#mountfrom = f"/home/{computer['user']}",
					name = "dozzle",
					login = True,
					loggout = True,
					logg = False,
					macaddress = None,
					postClean = False,
					preClean = False,
					extra = "--volume=/var/run/docker.sock:/var/run/docker.sock"
				).string()
			]
			bare_run &= False
		elif args.inkscape:
			#cmds += [prefix + f" docker run -p 3000:3000 -v /home/{computer['user']}:/sync hoppscotch/hoppscotch:latest"]
			#cmds += [prefix + f" docker run --shm-size=512m -p 6901:6901 -v /home/{computer['user']}:/sync -e VNC_PW=password kasmweb/insomnia:1.12.0"]
			#args.ports += ["3000"]
			cmds += [
				dock(save_host_dir=savedir,network = network,
					docker = "docker",
					image = "kasmweb/inkscape:1.12.0",
					ports = [6901],
					cmd = None,
					#nocmd = True,
					dind = dind,
					shared = False,
					detach = detach,
					sudo = sudo,
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
		elif args.gsync:
			#cmds += [prefix + f" docker run -p 3000:3000 -v /home/{computer['user']}:/sync hoppscotch/hoppscotch:latest"]
			#cmds += [prefix + f" docker run --shm-size=512m -p 6901:6901 -v /home/{computer['user']}:/sync -e VNC_PW=password kasmweb/insomnia:1.12.0"]
			#args.ports += ["3000"]
			cmds += [
				dock(save_host_dir=savedir,network = network,
					docker = "docker",
					image = "frantzme/dev:gsync",
					ports = [6901],
					cmd = None,
					#nocmd = True,
					dind = dind,
					shared = False,
					detach = detach,
					sudo = sudo,
					remove = True,
					mountto = "/sync/",
					mountfrom = args.gsync,
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
		elif False and args.knime:
			cmds += [
				dock(save_host_dir=savedir,network = network,
					docker = "docker",
					image = "frantzme/knime:latest",
					ports = [6901],
					cmd = None,
					#nocmd = True,
					dind = dind,
					shared = False,
					detach = detach,
					sudo = sudo,
					remove = True,
					mountto = "/workspace",
					mountfrom = args.knime,
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
		elif args.knime:
			cmds += [ #https://hub.docker.com/r/openkbs/knime-vnc-docker/
				dock(save_host_dir=savedir,network = network,
					docker = "docker",
					image = "openkbs/knime-vnc-docker",
					ports = [6901],
					cmd = None,
					#nocmd = True,
					dind = dind,
					shared = False,
					detach = detach,
					sudo = sudo,
					remove = True,
					mountto = "/workspace",
					mountfrom = args.knime,
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
		elif args.ui:
			#cmds += [prefix + f" docker run -p 3000:3000 -v /home/{computer['user']}:/sync hoppscotch/hoppscotch:latest"]
			#cmds += [prefix + f" docker run --shm-size=512m -p 6901:6901 -v /home/{computer['user']}:/sync -e VNC_PW=password kasmweb/insomnia:1.12.0"]
			#args.ports += ["3000"]
			cmds += [
				dock(save_host_dir=savedir,network = network,
					docker = "docker",
					image = "frantzme/dev:ui",
					ports = [6901],
					cmd = None,
					#nocmd = True,
					dind = dind,
					shared = False,
					detach = detach,
					sudo = sudo,
					remove = True,
					mountto = "/sync",
					mountfrom = args.ui,
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
		elif args.ref:
			#cmds += [prefix + f" docker run -p 3000:3000 -v /home/{computer['user']}:/sync hoppscotch/hoppscotch:latest"]
			#cmds += [prefix + f" docker run --shm-size=512m -p 6901:6901 -v /home/{computer['user']}:/sync -e VNC_PW=password kasmweb/insomnia:1.12.0"]
			#args.ports += ["3000"]
			cmds += [
				dock(save_host_dir=savedir,network = network,
					docker = "docker",
					image = "frantzme/dev:ref",
					ports = [6901],
					cmd = None,
					#nocmd = True,
					dind = dind,
					shared = False,
					detach = detach,
					sudo = sudo,
					remove = True,
					mountto = "/sync",
					mountfrom = args.ref,
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
				dock(save_host_dir=savedir,network = network,
					docker = "docker",
					image = "ghcr.io/laniksj/dfimage",
					ports = [6901],
					#nocmd = True,
					cmd = None,
					dind = True,
					shared = False,
					detach = detach,
					sudo = sudo,
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
		elif args.dockerSwarm:
			#cmds += [prefix + f" docker pull {args.reverse} && {prefix} docker run --privileged=true -v /var/run/docker.sock:/var/run/docker.sock --rm ghcr.io/laniksj/dfimage {args.reverse}"]
			cmds += [dock(save_host_dir=savedir,network = network,
					docker = "docker",
					image = "swarmpit/install:1.9",
					#ports = [],#[6901],
					#nocmd = True,
					cmd = "",
					dind = True,
					shared = False,
					detach = detach,
					sudo = sudo,
					remove = True,
					#mountto = "/sync",
					#mountfrom = f"/home/{computer['user']}",
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
				dock(save_host_dir=savedir,network = network,
					docker = "docker",
					image = "jetbrains/qodana-python",
					ports = [6901],
					#nocmd = True,
					cmd = None,
					dind = True,
					shared = False,
					detach = detach,
					sudo = sudo,
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
				dock(save_host_dir=savedir,network = network,
					docker = "docker",
					image = "jetbrains/qodana-jvm-community",
					ports = [6901],
					#nocmd = True,
					cmd = None,
					dind = True,
					shared = False,
					detach = detach,
					sudo = sudo,
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
			#For Mobile, add the parameter ?mobile on
			#other parameters: https://github.com/JetBrains/projector-client/tree/d70818f74babf8049ba81acf302e56263fd8780e/projector-client-web#main-parameters
			#args.cmd = f"docker run --rm -it --privileged=true -v /var/run/docker.sock:/var/run/docker.sock -v {os.path.abspath(args.pycharm)}/:/project -p {try_port('8887')}:8887 registry.jetbrains.team/p/prj/containers/projector-pycharm-p".split()
			#cmds += [f" {sdock} run --rm -it --privileged=true -v /var/run/docker.sock:/var/run/docker.sock -v {os.path.abspath(args.pycharm)}/:/project -p {try_port('8887')}:8887  -p 3000-4000:3000-4000 frantzme/pycharm:latest"]
			cmds += [
				dock(save_host_dir=savedir,network = network,
					docker = "docker",
					image = "frantzme/pycharm:latest",
					ports = [8887],
					#nocmd = True,
					cmd = None,
					dind = True,
					shared = False,
					detach = detach,
					sudo = sudo,
					remove = True,
					mountto = "/sync/",#"/project/",
					mountfrom = args.pycharm,
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
		elif args.office:
			#https://hub.docker.com/r/linuxserver/libreoffice
			cmds += [
				dock(save_host_dir=savedir,network = network,
					docker = "docker",
					image = "lscr.io/linuxserver/libreoffice:latest",
					ports = [3000, 3001],
					#nocmd = True,
					cmd = None,
					dind = True,
					shared = False,
					detach = detach,
					sudo = sudo,
					remove = True,
					mountto = "/sync/",#"/project/",
					mountfrom = args.office,
					#name: str = "current_running"
					login = False,
					loggout = False,
					logg = False,
					macaddress = None,
					postClean = False,
					preClean = False,
					extra = "-e PUID=1000 -e PGID=1000 -e TZ=Etc/UTC"
				).string()
			]
			bare_run &= False
		elif args.runme:
			#https://hub.docker.com/r/statefulhq/runme
			cmds += [
				dock(save_host_dir=savedir,network = network,
					docker = "docker",
					image = "statefulhq/runme:latest",
					ports = [8080],
					#nocmd = True,
					cmd = args.runme,
					dind = True,
					shared = False,
					detach = detach,
					sudo = sudo,
					remove = True,
					mountto = "/sync/",#"/project/",
					mountfrom = ":!",
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
			#runme
		elif args.mrust:
			cmds += [
				dock(save_host_dir=savedir,network = network,
					docker = "docker",
					image = "rust:slim-buster",
					ports = [],
					#nocmd = True,
					cmd = None,
					dind = dind,
					shared = False,
					detach = detach,
					sudo = sudo,
					remove = True,
					mountto = "/sync/",#"/project/",
					mountfrom = args.mrust,
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
		elif args.webstorm:
			#https://stackoverflow.com/questions/28717464/docker-expose-all-ports-or-range-of-ports-from-7000-to-8000
			#args.cmd = f"docker run --rm -it --privileged=true -v /var/run/docker.sock:/var/run/docker.sock -v {os.path.abspath(args.pycharm)}/:/project -p {try_port('8887')}:8887 registry.jetbrains.team/p/prj/containers/projector-pycharm-p".split()
			#cmds += [f" {sdock} run --rm -it --privileged=true -v /var/run/docker.sock:/var/run/docker.sock -v {os.path.abspath(args.pycharm)}/:/project -p {try_port('8887')}:8887  -p 3000-4000:3000-4000 frantzme/pycharm:latest"]
			cmds += [
				dock(save_host_dir=savedir,network = network,
					docker = "docker",
					image = "registry.jetbrains.team/p/prj/containers/projector-webstorm",#"frantzme/webstorm:latest",
					ports = [8887],
					#nocmd = True,
					cmd = None,
					dind = True,
					shared = False,
					detach = detach,
					sudo = sudo,
					remove = True,
					mountto = "/sync/",#"/project/",
					mountfrom = args.webstorm,
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
		elif args.redirect:
			#https://shlink.io/documentation/install-docker-image/
			cmds += [
				dock(save_host_dir=savedir,network = network,
					docker = "docker",
					image = "shlinkio/shlink:stable",
					ports = [8080],
					#nocmd = True,
					cmd = None,
					dind = dind,
					shared = False,
					detach = True,
					sudo = sudo,
					remove = True,
					mountto = "/sync/",#"/project/",
					#mountfrom = args.pycharm,
					name = "redirector",
					login = False,
					loggout = False,
					logg = False,
					macaddress = None,
					postClean = False,
					preClean = False,
					extra = "-e DEFAULT_DOMAIN=localhost -e IS_HTTPS_ENABLED=false"
				).string()
			]
			bare_run &= False
		elif args.swaggergenpy:
			#https://github.com/swagger-api/swagger-codegen#public-pre-built-docker-images
			cmds += [
				dock(save_host_dir=savedir,network = network,
					docker = "docker",
					image = "swaggerapi/swagger-codegen-cli:latest",
					ports = [],
					#nocmd = False,
					cmd = """generate -i {0} -l python -o /local/py_gen """.format(args.swaggergenpy),
					dind = True,
					shared = False,
					detach = detach,
					sudo = sudo,
					remove = True,
					mountto = "/local/",
					mountfrom = os.path.abspath(os.curdir),
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
		elif args.dejs:
			# https://hub.docker.com/r/remnux/de4js
			# https://www.github.com/REMnux/docker
			# https://github.com/lelinhtinh/de4js/blob/master/Dockerfile
			# docker run -d --rm -p 4000:4000 -p 35729:35729 --name de4js remnux/de4js
			print("Copy and paste the command: <bundle install --retry 5 --jobs 20 && bundle exec jekyll serve --host 0.0.0.0>")
			cmds += [
				dock(save_host_dir=savedir,network = network,
					docker = "docker",
					image = "remnux/de4js",
					ports = [4000, 35729],
					#nocmd = True,
					cmd = None,
					dind = True,
					shared = False,
					detach = detach,
					sudo = sudo,
					remove = True,
					mountto = "/sync/",
					mountfrom = args.dejs,
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
				dock(save_host_dir=savedir,network = network,
					docker = "docker",
					image = "frantzme/intellij:latest",
					ports = [8887],
					#nocmd = True,
					cmd = None,
					dind = True,
					shared = False,
					detach = detach,
					sudo = sudo,
					remove = True,
					mountto = "/sync/",
					mountfrom = args.intellij,
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
				dock(save_host_dir=savedir,network = network,
					docker = "docker",
					image = "frantzme/datagrip:latest",
					ports = [8887],
					#nocmd = True,
					cmd = None,
					dind = True,
					shared = False,
					detach = detach,
					sudo = sudo,
					remove = True,
					mountto = "/sync/",#"/project/",
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
		elif args.ball:
			#args.cmd = f"sudo docker run --rm -it --privileged=true -v /var/run/docker.sock:/var/run/docker.sock -v {os.path.abspath(args.intellij)}/:/project -p {try_port('8887')}:8887 registry.jetbrains.team/p/prj/containers/projector-idea-u".split()
			#cmds += [f" {sdock} run --rm -it --privileged=true -v /var/run/docker.sock:/var/run/docker.sock -v {os.path.abspath(args.ball)}/:/project -p {try_port('8887')}:8887  -p 3000-4000:3000-4000 frantzme/mygrip:latest"]
			cmds += [
				dock(save_host_dir=savedir,network = network,
					docker = "docker",
					image = "frantzme/ballerina:lite",
					ports = [8887, 8888, 8912],
					#nocmd = True,
					cmd = None,
					dind = True,
					shared = False,
					detach = detach,
					sudo = sudo,
					remove = True,
					mountto = "/sync/",#"/project/",
					mountfrom = os.path.abspath(args.ball),
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
		elif args.grist:
			#https://github.com/gristlabs/grist-core
			#args.cmd = f"sudo docker run --rm -it --privileged=true -v /var/run/docker.sock:/var/run/docker.sock -v {os.path.abspath(args.intellij)}/:/project -p {try_port('8887')}:8887 registry.jetbrains.team/p/prj/containers/projector-idea-u".split()
			#cmds += [f" {sdock} run --rm -it --privileged=true -v /var/run/docker.sock:/var/run/docker.sock -v {os.path.abspath(args.datagrip)}/:/project -p {try_port('8887')}:8887  -p 3000-4000:3000-4000 frantzme/mygrip:latest"]
			cmds += [
				dock(save_host_dir=savedir,network = network,
					docker = "docker",
					image = "gristlabs/grist:latest",
					ports = [8484],
					#nocmd = True,
					cmd = " ",
					dind = True,
					shared = False,
					detach = detach,
					sudo = sudo,
					remove = True,
					mountto = "/persist/",#"/project/",
					mountfrom = os.path.abspath(args.grist),
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
		elif bare_run:
			ports = "";import sdock
			for port in args.ports:
				ports += f" -L {sdock.util.getPort([port], prefix='', dup=False)}:{computer['ip']}:{port} "

			cmds += [run(computer,' '.join(args.cmd), ports)]

	for x in cmds:
		print(x)
		if not args.print:
			os.system(x)
