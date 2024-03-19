#!/usr/bin/env python3

import os,sys

#From :> https://ammonite.io/#Reference

cmd = """sudo sh -c '(echo "#!/usr/bin/env sh" && curl -L https://github.com/com-lihaoyi/Ammonite/releases/download/3.0.0-M1/2.12-3.0.0-M1) > /usr/local/bin/amm && chmod +x /usr/local/bin/amm' && amm"""

print(cmd);

try:os.system(cmd)
except:pass


try:os.system(cmd.replace("sudo ", ""))
except:pass