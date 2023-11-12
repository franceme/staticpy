#!/usr/bin/python3
import os,sys,time

"""
https://github.com/tqdm/tqdm
https://github.com/tmux-python/libtmux
"""
try:
	import libtmux
	from tqdm import tqdm
except:
	os.system("{0} -m pip install --upgrade tqdm libtmux".format(sys.executable))
	import libtmux
	from tqdm import tqdm

def getArgs():
	import argparse
	parser = argparse.ArgumentParser("Mux Expanding aide")
	parser.add_argument("--grace", help="Start the Grace mux session",action='store_true',default=False)
	parser.add_argument("--pybase", help="Start Python Based mux session",action='store_true',default=False)
	parser.add_argument("--crypto", help="Start the Grace mux session",action='store_true',default=False)
	parser.add_argument("--clean", help="Clean the mux session",action='store_true',default=False)
	return parser.parse_args()

def wait(num):
	for _ in tqdm(range(num)):
		time.sleep(1)

def send_key_in_window(window, command, enter=False):
	t_pane = window.panes[0]
	send_key_in_pane(t_pane, command, enter=enter)

def send_key_in_pane(t_pane, command, enter=False):
	t_pane.send_keys(command, enter=enter)

def main(argz):
	s = libtmux.Server()

	if argz.grace:
		projects = os.path.join(os.path.expanduser("~"), "Projects")
		prelim_session = s.new_session(session_name="grace",attach=False,start_directory=projects)
		prelim_window = prelim_session.attached_window

		bottom = prelim_window.split_window(start_directory=projects, vertical=True)
		bottom.key = lambda key,enter=True:send_key_in_pane(bottom, key, enter)

		right = prelim_window.split_window(start_directory=projects,percent=25, vertical=False)
		right.key = lambda key,enter=True:send_key_in_pane(right, key, enter)
		#send_key_in_pane(right,"echo RIGHT", True)

		midRight = prelim_window.split_window(start_directory=projects,percent=35, vertical=False)
		midRight.key = lambda key,enter=True:send_key_in_pane(midRight, key, enter)
		#send_key_in_pane(midRight,"echo MIDDLERight", True)

		midLeft = prelim_window.split_window(start_directory=projects,percent=50, vertical=False)
		midLeft.key = lambda key,enter=True:send_key_in_pane(midLeft, key, enter)
		#send_key_in_pane(midLeft,"echo MIDDLELEFT", True)

		left = prelim_window.split_window(start_directory=projects,percent=95, vertical=False)
		left.key = lambda key,enter=True:send_key_in_pane(left, key, enter)
		#send_key_in_pane(left,"echo LEFT", True)
		#left.key("echo LEFT")

		#bottom.key("dock.sh --clean")
		wait(30)

		left.key("""docker run --privileged=true -v /var/run/docker.sock:/var/run/docker.sock --network="host" --rm -it -v "`pwd`:/sync"   -p 8912:8912     frantzme/ballerina:lite /bin/bash""")
		left.key("vs");left.key("vs")

		midLeft.key("""docker run  --rm -it -v "`pwd`:/sync"   -p 8000:8000  -e SPLUNK_START_ARGS='--accept-license' -e SPLUNK_PASSWORD='password' --network="host"  splunk/splunk:latest start""")

		midRight.key("""dock.sh --shorty""")
		midRight.key("ez -a")
		midRight.key("ez -z -l frantzme@vt.edu")

		right.key("""dock.sh --shorty""")
		right.key("""xonsh""")

		loggingWindow = s.new_window(session_name="grace", attach=False, window_name="Logging")
		loggingWindow.split_window(start_directory=projects, vertical=True)
		send_key_in_pane(loggingWindow.panes[0], "python3 testfunnel/follow.py -f testfunnel/originallog.jsonl", True)
		send_key_in_pane(loggingWindow.panes[1], "python3 testfunnel/follow.py -f testfunnel/browser.log", True)

	if argz.crypto:
		projects = os.path.join(os.path.expanduser("~"), "Projects")
		start_session = s.new_session(session_name="crypto",attach=False,start_directory=projects)
		prelim_window = start_session.attached_window
		prelim_window.key = lambda key, enter=True:send_key_in_window(prelim_window, key, enter=enter)

		prelim_window.key("dock.sh --shorty")
		wait(30)
		prelim_window.key("ez -a")
		prelim_window.key("ez -z -l frantzme@vt.edu")
		wait(20)
		prelim_window.key("git clone git@github.com:franceme/cry")

		loggingWindow = session.new_window(session_name="crypto",attach=False, window_name="Logging")

		bottom = prelim_window.split_window(start_directory=projects, vertical=True)
		bottom.key = lambda key,enter=True:send_key_in_pane(bottom, key, enter)

		right = prelim_window.split_window(start_directory=projects,percent=25, vertical=False)
		right.key = lambda key,enter=True:send_key_in_pane(right, key, enter)
		#send_key_in_pane(right,"echo RIGHT", True)

		midRight = prelim_window.split_window(start_directory=projects,percent=35, vertical=False)
		midRight.key = lambda key,enter=True:send_key_in_pane(midRight, key, enter)
		#send_key_in_pane(midRight,"echo MIDDLERight", True)

		midLeft = prelim_window.split_window(start_directory=projects,percent=50, vertical=False)
		midLeft.key = lambda key,enter=True:send_key_in_pane(midLeft, key, enter)
		#send_key_in_pane(midLeft,"echo MIDDLELEFT", True)

		left = prelim_window.split_window(start_directory=projects,percent=95, vertical=False)
		left.key = lambda key,enter=True:send_key_in_pane(left, key, enter)
		#send_key_in_pane(left,"echo LEFT", True)
		#left.key("echo LEFT")

		#bottom.key("dock.sh --clean")
		wait(30)

		left.key("""docker run --privileged=true -v /var/run/docker.sock:/var/run/docker.sock --network="host" --rm -it -v "`pwd`:/sync"   -p 8912:8912     frantzme/ballerina:lite /bin/bash""")
		left.key("vs");left.key("vs")

		midLeft.key("""docker run  --rm -it -v "`pwd`:/sync"   -p 8000:8000  -e SPLUNK_START_ARGS='--accept-license' -e SPLUNK_PASSWORD='password' --network="host"  splunk/splunk:latest start""")

		midRight.key("""dock.sh --shorty""")
		midRight.key("ez -a")
		midRight.key("ez -z -l frantzme@vt.edu")

		right.key("""dock.sh --shorty""")
		right.key("""xonsh""")

		loggingWindow = session.new_window(attach=False, window_name="Logging")
		loggingWindow.split_window(start_directory=projects, vertical=True)
		send_key_in_pane(loggingWindow.panes[0], "python3 testfunnel/follow.py -f testfunnel/originallog.jsonl", True)
		send_key_in_pane(loggingWindow.panes[1], "python3 testfunnel/follow.py -f testfunnel/browser.log", True)

	if args.pybase:
		projects = os.path.join(os.path.expanduser("~"), "Projects")
		session = s.new_session(session_name="pybase",attach=False,start_directory=projects)
		window = session.attached_window

		bottom = window.split_window(start_directory=projects, vertical=True)
		bottom.key = lambda key,enter=True:send_key_in_pane(bottom, key, enter)

		right = window.split_window(start_directory=projects,percent=25, vertical=False)
		right.key = lambda key,enter=True:send_key_in_pane(right, key, enter)

		midRight = window.split_window(start_directory=projects,percent=35, vertical=False)
		midRight.key = lambda key,enter=True:send_key_in_pane(midRight, key, enter)

		midLeft = window.split_window(start_directory=projects,percent=50, vertical=False)
		midLeft.key = lambda key,enter=True:send_key_in_pane(midLeft, key, enter)

		left = window.split_window(start_directory=projects,percent=95, vertical=False)
		left.key = lambda key,enter=True:send_key_in_pane(left, key, enter)

		wait(30)

		left.key("""dock.sh --short3 --network ~""")
		left.key("vs");left.key("vs")

		midLeft.key("""zz -n self --splunk --network ~""")

		midRight.key("""zz -n self --pycharm :! --network ~""")

		right.key("""dock.sh --shorty""")
		right.key("ez -a")
		right.key("ez -z -l frantzme@vt.edu")

	if argz.clean:
		try:
			for session in s.sessions:
				for window in session.windows:
					window.kill_window()
		except: pass


if __name__ == '__main__':
	main(getArgs())
