#!/usr/bin/env python3
#https://philstories.medium.com/connect-jetbrains-ide-intellj-to-github-codespace-47c51966b650

import os,sys

def run(string):
    print(string)
    os.system(string)

containerName = "<>"
if len(sys.argv) >= 2:
    containerName = sys.argv[1]

for cmd in [
    "gh auth login",
    "gh auth refresh -h github.com -s codespace",
    #"gh codespace ssh",

    "gh codespace ssh --config >> ~/.ssh/config",
    "cat ~/.ssh/codespaces"
]:
    run(cmd)

with open("~/.ssh/codespaces","a+") as writer:
    writer.write(f"""
Host {containerName}.dev-container
    User vscode
    ProxyCommand /usr/local/bin/gh cs ssh -c {containerName} --stdio
    UserKnownHostsFile=/dev/null
    StrictHostKeyChecking no
    LogLevel quiet
    ControlMaster auto
""")
