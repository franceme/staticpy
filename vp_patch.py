import os,sys

def run(string):
	print(string);os.system(string)

def getArgs():
	import argparse
	parser = argparse.ArgumentParser("Patch the virtualbox to disable time load")
	parser.add_argument("-n","--name", help="The name of the virtualbox to patch",nargs=1, default=None)
	return parser.parse_args()

def step_one(vname):
	return """VBoxManage setextradata "{0}" "VBoxInternal/Devices/VMMDev/0/Config/GetHostTimeDisabled" 1""".format(vname)

def step_two(vname, time_to_set_to=None):
	time_to_set = "-31536000000"
	"""
	https://developer.microsoft.com/en-us/microsoft-edge/tools/vms/
The only way is to set the time in the Virtualbox motherboard using the command line:

VBoxManage modifyvm <name> --biossystemtimeoffset <msec>

For example, to set back the date 1 year:

VBoxManage modifyvm <name> --biossystemtimeoffset -31536000000

In XML File (add GetHostTimeDisabled:
<?xml version="1.0"?>
<!--
 DO NOT EDIT THIS FILE.
 If you make changes to this file while any VirtualBox related application
 is running, your changes will be overwritten later, without taking effect.
 Use VBoxManage or the VirtualBox Manager GUI to make changes.
-->
<VirtualBox xmlns="http://www.virtualbox.org/" version="1.15-windows">
  <Machine uuid="{9a2a4984-c683-4707-b522-9eefbbd0e553}" name="Windows_365" OSType="Windows10_64" currentSnapshot="{0ebf0789-d564-4ce2-bc64-3c3e740368b2}" snapshotFolder="Snapshots" currentStateModified="false" lastStateChange="2021-01-27T13:13:13Z">
    <MediaRegistry>
      <HardDisks>
        <HardDisk uuid="{4193cbbe-61f3-4db1-aae2-648cbfd39e1c}" location="Windows_365-disk001.vdi" format="vdi" type="Normal">
          <HardDisk uuid="{da62a9a9-6818-4836-897a-3f66c9f07908}" location="Snapshots/{da62a9a9-6818-4836-897a-3f66c9f07908}.vdi" format="vdi"/>
        </HardDisk>
      </HardDisks>
    </MediaRegistry>
    <ExtraData>
      <ExtraDataItem name="GUI/LastCloseAction" value="PowerOff"/>
      <ExtraDataItem name="GUI/LastGuestSizeHint" value="1920,1034"/>
      <ExtraDataItem name="GUI/LastNormalWindowPosition" value="0,24,640,480,max"/>
      <ExtraDataItem name="VBoxInternal/Devices/VMMDev/0/Config/GetHostTimeDisabled" value="1"/>

#VBox #VM #Date #Virtual #Windows #Window #ISO #iso
	"""
	return """VBoxManage modifyvm "{0}" --biossystemtimeoffset {1}""".format(vname, time_to_set)

if __name__ == '__main__':
	args = getArgs()
	vname = str(args.name[0]).strip()
	for step in [
		step_one,
		#step_two,
	]:
		run(step(vname))