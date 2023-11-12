import os,sys


def getArgs():
	import argparse
	parser = argparse.ArgumentParser("Install Things")
	parser.add_argument("--docker", help="Install Docker",action='store_true',default=False)
	parser.add_argument("--dockerSwarm", help="Install Docker and setup Docker Swarm",action='store_true',default=False)
	args,unknown = parser.parse_known_args()
	return args


if __name__ == "__main__":
    args = getArgs()

    if args.docker or args.dockerSwarm:
        try:
            import sdock
        except:
            os.system("{0} -m pip install --upgrade sdock".format(sys.executable))
            import sdock

        sdock.install_docker()
    if args.dockerSwarm:
        print()
        #https://github.com/swarmpit/swarmpit
        #https://docs.docker.com/engine/swarm/key-concepts/
        #https://github.com/moby/swarmkit

        """
        https://github.com/docker/docker-py
        
        """