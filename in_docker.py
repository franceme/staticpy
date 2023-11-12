import os,sys

try:
    import sdock
except:
    os.system("{0} -m pip install --upgrade sdock".format(sys.executable))
    import sdock

sdock.install_docker()
print("Completed")