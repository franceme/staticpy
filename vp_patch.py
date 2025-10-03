#!/usr/bin/env python3

import os
import time
import sys
import typing
import argparse
import shutil
import datetime
import pathlib
import subprocess
import tempfile
import configargparse

vboxmanage: typing.Optional[str] = shutil.which(cmd="VBoxManage")
if vboxmanage is None:
    raise Exception("Need to have a path for the vboxmanage script")

def diff_in_milliseconds(previous_datetime: datetime.datetime, current_datetime:typing.Optional[datetime.datetime]=None) -> int:
    """
    Calculates the difference in milliseconds between two datetime objects.

        previous_datetime (datetime.datetime): The earlier datetime to compare.
        current_datetime (typing.Optional[datetime.datetime], optional): The later datetime to compare. 
            If None, the current date and time is used.

        int: The difference in milliseconds between previous_datetime and current_datetime.
             The result is positive if previous_datetime is after current_datetime, negative otherwise.
    """
    if current_datetime is None:
        current_datetime = datetime.datetime.now()

    return int((previous_datetime - current_datetime).total_seconds() * 1000)

class VBoxManager(object):
    def __show_wait_for(self, time_seconds: int) -> None:
        for remaining in range(time_seconds, 0, -1):
            sys.stdout.write(f"\rWaiting {remaining} seconds... ")
            sys.stdout.flush()
            time.sleep(1)
        print("\r" + " " * 30 + "\r", end="")  # Clear the line after waiting

    def __init__(self, vm_file:str, vm_name:typing.Optional[str]=""):
        self.vm_file:str = vm_file
        self.vm_name:str = vm_name or os.path.basename(str(vm_file)).replace('.ova','')
        self.linux_base:bool = sys.platform.startswith('linux') or sys.platform == 'darwin'

    def unset_timesync(self):
        #<ExtraDataItem name="VBoxInternal/Devices/VMMDev/0/Config/GetHostTimeDisabled" value="1"/>
        self.__vboxmanage(
            f"""setextradata {self.vm_name} "VBoxInternal/Devices/VMMDev/0/Config/GetHostTimeDisabled" "1" """
        )

    def set_date(self, vm_date:datetime.datetime):
        #VBoxManage modifyvm <name> --biossystemtimeoffset <msec>
        self.__vboxmanage(
            f"""modifyvm {self.vm_name} --biossystemtimeoffset {diff_in_milliseconds(previous_datetime=vm_date)}"""
        )

    def __vboxmanage(self, command:str, time_to_wait_for:int=5) -> str:
        cmd:str = f"""{vboxmanage} {command}"""
        print(cmd)

        if not self.linux_base:
            process = subprocess.Popen(
                args=cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = process.communicate()

            self.__show_wait_for(time_seconds=time_to_wait_for)

            if process.returncode != 0:
                raise Exception(f"Error running command {cmd}: {stderr}")

            return stdout


        with tempfile.NamedTemporaryFile(mode='w+', delete=True) as stdout_file, tempfile.NamedTemporaryFile(mode='w+', delete=True) as stderr_file:
            process = subprocess.Popen(
                args=f"""{cmd} 1>> "{stdout_file.name}" 2>> "{stderr_file.name}" """,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            last_stdout_size    : float = 0
            last_stderr_size    : float = 0
            poll_interval       : float=.1
            stdout_content      : str = ""
            stderr_content      : str = ""

            try:
                while process.poll() is None:
                    # Monitor stdout
                    if os.path.exists(stdout_file.name):
                        with open(stdout_file.name, 'r') as f:
                            f.seek(last_stdout_size)
                            new_content = f.read()
                            if new_content:
                                print(new_content, end='')
                                stdout_content += new_content
                            last_stdout_size = f.tell()
                    # Monitor stderr
                    if os.path.exists(stderr_file.name):
                        with open(stderr_file.name, 'r') as f:
                            f.seek(last_stderr_size)
                            new_content = f.read()
                            if new_content:
                                print(new_content, end='', file=sys.stderr)
                                stderr_content += new_content
                            last_stderr_size = f.tell()
                    time.sleep(poll_interval)
            finally:
                # Print and collect any remaining content after process ends
                if os.path.exists(stdout_file.name):
                    with open(stdout_file.name, 'r') as f:
                        f.seek(last_stdout_size)
                        new_content = f.read()
                        if new_content:
                            print(new_content, end='')
                            stdout_content += new_content
                if os.path.exists(stderr_file.name):
                    with open(stderr_file.name, 'r') as f:
                        f.seek(last_stderr_size)
                        new_content = f.read()
                        if new_content:
                            print(new_content, end='', file=sys.stderr)
                            stderr_content += new_content

            if process.returncode != 0:
                raise Exception(f"Error running command {cmd}: {stderr_content}")

            return stdout_content

    def vm_exe(self, command:str, user:str="root", password:str="root", shell:str="/bin/sh") -> str:
        return self.__vboxmanage(
            f"""guestcontrol {self.vm_name} run --exe "{shell}" --username {user} --password {password} -- -c '{command}'"""
        )

    def load(self):
        print(f"Loading VM from {self.vm_file} as {self.vm_name}")
        self.__vboxmanage(
            f"""import {self.vm_file} --vsys 0 --vmname {self.vm_name}""",
            time_to_wait_for=20
        )
    
    def online(self):
        print(f"Starting VM {self.vm_name}")
        self.__vboxmanage(
            f"""startvm {self.vm_name} --type headless"""
        )

    def offline(self, force:bool=False):
        print(f"Stopping VM {self.vm_name}")
        self.__vboxmanage(
            f"""controlvm {self.vm_name} {'acpipowerbutton' if force else 'poweroff'}"""
        )

    def remove(self):
        print(f"Removing VM {self.vm_name}")
        self.__vboxmanage(
            f"""unregistervm {self.vm_name} --delete"""
        )

    def add_shared_folder(self, folder_name:str, host_path:str, automount:bool=True, make_permanent:bool=True):
        self.__vboxmanage(
            f"""sharedfolder add {self.vm_name} --name "{folder_name}" --hostpath "{host_path}" {'--automount' if automount else ''} {'--permanent' if make_permanent else ''}"""
        )
    
    def list_shared_folders(self) -> typing.List[str]:
        return self.__vboxmanage(
            f"""sharedfolder list {self.vm_name}"""
        ).splitlines()

    def add_file(self, source_path:str, dest_path:str, user:str="root", password:str="root", shell:str="/bin/sh"):
        self.__vboxmanage(
            f"""guestcontrol {self.vm_name} copyto "{source_path}" "{dest_path}" --username {user} --password {password} --shell {shell}"""
        )

    def disable_network_adapter(self, adapter_number:int=1):
        self.__vboxmanage(
            f"""modifyvm {self.vm_name} --nic{adapter_number} none"""
        )

    #region Snapshots
    def snapshot_take(self, snapshot_name:str):
        self.__vboxmanage(
            f"""snapshot {self.vm_name} take "{snapshot_name}" """
        )

    def snapshot_restore(self, snapshot_name:str):
        self.__vboxmanage(
            f"""snapshot {self.vm_name} restore "{snapshot_name}" """
        )

    def snapshot_delete(self, snapshot_name:str):
        self.__vboxmanage(
            f"""snapshot {self.vm_name} delete "{snapshot_name}" """
        )

    def snapshot_list(self) -> typing.List[str]:
        return self.__vboxmanage(
            f"""snapshot {self.vm_name} list"""
        ).splitlines()
    #endregion

    def info(self) -> str:
        return self.__vboxmanage(
            f"""showvminfo {self.vm_name}"""
        )
    
    def list(self) -> typing.Dict[str, str]:
        output:typing.Dict[str,str] = {}
        for line in self.__vboxmanage(
            f"""list vms"""
        ).splitlines():
            if line.strip() != '':
                parts = line.split(' ')
                name = ' '.join(parts[:-1]).strip('"')
                uuid = parts[-1].strip('{}')
                output[name] = uuid
        
        return output


def parse_args() -> configargparse.Namespace:
    # region Valdiators
    def generate_file_validation_by_ext(fileext:str):
        def validate_existing_file(filepath_str:str) -> pathlib.Path:
            """
            Custom type function to validate if a given path is an existing file.
            Returns a pathlib.Path object if valid, raises an error otherwise.
            """
            path = pathlib.Path(filepath_str)
            if not path.is_file():
                raise argparse.ArgumentTypeError(f"'{filepath_str}' is not a valid file or does not exist.")
            elif not filepath_str.endswith(fileext):
                raise argparse.ArgumentTypeError(f"'{filepath_str}' is not the right file type.")
            return path

        return validate_existing_file

    def parse_datetime(date_string:str) -> datetime.datetime:
        """
        Custom type function to parse a date string into a datetime object.
        You can adjust the format string ('%Y-%m-%d') as needed.
        """
        try:
            return datetime.datetime.strptime(date_string, '%Y-%m-%d')
        except ValueError:
            raise argparse.ArgumentTypeError(
                f"Invalid datetime format: '{date_string}'. Expected format: YYYY-MM-DD"
            )
    # endregion

    parser = configargparse.ArgumentParser(
        default_config_files=['config.yaml'],
        config_file_parser_class=configargparse.YAMLConfigFileParser,
        description="Manage a VM via VBoxManage"
    )

    parser.add_argument(
        "--ova",
        type=generate_file_validation_by_ext(".ova"),
        required=True,
        help="The ova file to import"
    )

    parser.add_argument(
        "--load",
        action="store_true",
        help="Whether to load the VM if not already loaded"
    )

    parser.add_argument(
        "--on",
        action="store_true",
        help="Whether to turn the VM on"
    )

    parser.add_argument(
        "--off",
        action="store_true",
        help="Whether to turn the VM off"
    )

    parser.add_argument(
        "--take_snapshot",
        type=str,
        help="The name of the snapshot to take"
    )

    parser.add_argument(
        "--restore_snapshot",
        type=str,
        help="The name of the snapshot to restore"
    )

    parser.add_argument(
        "--set_date",
        type=parse_datetime,
        help="The date to set the vm to"
    )

    parser.add_argument(
        "--remove",
        action="store_true",
        help="Whether to remove the VM"
    )

    parser.add_argument(
        "--unset_timesync",
        action="store_true",
        help="Whether to unset the timesync"
    )

    parser.add_argument(
        "--info",
        action="store_true",
        help="Whether to show info about the VM"
    )

    parser.add_argument(
        "--command_after_load",
        type=str,
        help="A command to run inside the VM after loading it"
    )

    parser.add_argument(
        "--command_after_on",
        type=str,
        help="A command to run inside the VM after booting it"
    )

    parser.add_argument(
        "--add_shared_folder",
        nargs=2,
        metavar=('FOLDER_NAME', 'HOST_PATH'),
        help="Add a shared folder to the VM. Provide FOLDER_NAME and HOST_PATH."
    )

    parser.add_argument(
        "--add_file",
        nargs=2,
        metavar=('SOURCE_PATH', 'DEST_PATH'),
        help="Add a file to the VM. Provide SOURCE_PATH and DEST_PATH."
    )

    parser.add_argument(
        "--disable_network_adapter",
        action="store_true",
        help="Disable the first network adapter of the VM"
    )

    parser.add_argument(
        "--command_before_off",
        type=str,
        help="A command to run inside the VM before booting it"
    )

    return parser.parse_args()

if __name__ == "__main__":
    args: argparse.Namespace = parse_args()

    mgr = VBoxManager(
        vm_file=args.ova
    )

    if args.info:
        print(mgr.info())
        sys.exit(0)

    if args.load and mgr.vm_name not in mgr.list():
        mgr.load()
        mgr.snapshot_take(
            snapshot_name=f"Initial setup {args.date.strftime('%Y-%m-%d')}"
        )
        if args.command_after_load is not None:
            args.on()
            print(mgr.vm_exe(command=args.command_after_load))
            args.off()
    
    if args.unset_timesync:
        mgr.unset_timesync()

    if args.set_date is not None:
        mgr.set_date(
            vm_date=args.set_date
        )

    if args.disable_network_adapter:
        mgr.disable_network_adapter(adapter_number=1)

    if args.on:
        mgr.online()

        if args.command_after_on is not None:
            print(mgr.vm_exe(command=args.command_after_on))

    if args.add_shared_folder and args.add_shared_folder[1] not in mgr.list_shared_folders():
        mgr.add_shared_folder(
            folder_name=args.add_shared_folder[0],
            host_path=args.add_shared_folder[1]
        )
    
    if args.add_file:
        mgr.add_file(
            source_path=args.add_file[0],
            dest_path=args.add_file[1]
        )

    if args.take_snapshot is not None:
        mgr.snapshot_take(
            snapshot_name=args.take_snapshot
        )
    
    if args.restore_snapshot is not None:
        mgr.snapshot_restore(
            snapshot_name=args.restore_snapshot
        )

    if args.off:
        if args.command_before_off is not None:
            print(mgr.vm_exe(command=args.command_before_off))

        mgr.offline(force=False)

    if args.remove:
        try:mgr.offline(force=False)
        except:pass
        mgr.remove()
