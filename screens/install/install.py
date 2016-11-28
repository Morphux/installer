################################### LICENSE ####################################
#                            Copyright 2016 Morphux                            #
#                                                                              #
#        Licensed under the Apache License, Version 2.0 (the "License");       #
#        you may not use this file except in compliance with the License.      #
#                  You may obtain a copy of the License at                     #
#                                                                              #
#                 http://www.apache.org/licenses/LICENSE-2.0                   #
#                                                                              #
#      Unless required by applicable law or agreed to in writing, software     #
#       distributed under the License is distributed on an "AS IS" BASIS,      #
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  #
#        See the License for the specific language governing permissions and   #
#                       limitations under the License.                         #
################################################################################

##
# install.py
# Created: 25/11/2016
# By: Louis Solofrizzo <louis@morphux.org>
##

import      json
import      os
from        subprocess import Popen, PIPE, STDOUT, call

class   Install:

##
# Variables
##

    dlg = 0 # Dialog object
    conf_lst = {} # List object for configuration
    modules = {} # Module object
    pkgs = {} # Packages instances

##
# Functions
##

    # Init function, called by Main instance
    def init(self, dialog, config_list):
        self.dlg = dialog
        self.conf_lst = config_list
        self.config = {
            "id": 6,
            "name": "Install"
        }
        return self.config

    # main function, called by Main instance
    def     main(self, Main):
        # The current configuration is already loaded from a file, no
        # reason to re-save it.
        if "load_conf" not in self.conf_lst:
            code = self.dlg.yesno("Do you want to save your current configuration ?")
            if code == "ok":
                # Open the file, then dump json in it.
                with open("morphux_install.conf", "w") as fd:
                    json.dump(self.conf_lst, fd)

        # Load packages files
        self.load_pkgs()

        # If partitionning is needed, do it
        if "partitionning.disk.format" in self.conf_lst:
            self.create_partitions()
        self.format()

    # Load all the packages configuration files
    # path: Default to ./pkgs
    def     load_pkgs(self, path = "pkgs"):
        res = {}
        lst = os.listdir(path)
        dir = []
        # List the entries in screens/ and check if the file __init__.py is here
        for d in lst:
            s = os.path.abspath(path) + os.sep + d
            if os.path.isdir(s) and os.path.exists(s + os.sep + "__init__.py"):
                dir.append(d)
        # Import the good files, in order to load them
        for d in dir:
            res[d] = __import__(path + "." + d + "." + d, fromlist = ["*"])
            res[d] = getattr(res[d], d.title())
        self.modules = res
        self.get_pkg_info()

    # Get information about each package, and instanciate them
    def     get_pkg_info(self):
        config = {}
        for name, klass in self.modules.items():
            print("Reading info on "+ name +" ...", end="")
            klass = klass()
            # Calling the init function of each package
            config = klass.init(self.conf_lst)
            # Saving the configuration of the object
            self.pkgs[config["name"]] = [klass, config]
            print("\tDone !")

    # Function that format disk and create new partitions
    def     create_partitions(self):
        # Object used to define types in fdisk
        types = {
            "Grub": "21686148-6449-6E6F-744E-656564454649",
            "Boot": "0FC63DAF-8483-4772-8E79-3D69D8477DE4",
            "Root": "0FC63DAF-8483-4772-8E79-3D69D8477DE4",
            "Home": "0FC63DAF-8483-4772-8E79-3D69D8477DE4",
            "Tmp": "0FC63DAF-8483-4772-8E79-3D69D8477DE4",
            "Swap": "0657FD6D-A4AB-43C4-84E5-0933C84B4F4F"
        }

        layout = self.conf_lst["partitionning.layout"] # Partition future layout
        disk = self.conf_lst["partitionning.disk"] # Disk used for partitionning

        # Creating a new partiton label
        self.dlg.infobox("Creating a new partition table on "+ disk+ "...",
            width=50, height=3)
        self.fdisk(["g", "p", "w"], disk)

        # List partitions to add
        i = 0
        for p in layout:
            if p["disk"] == disk:
                self.dlg.infobox("Creating partition"+ p["part"] +"...",
                    width=50, height=3)
                self.fdisk(["n", p["part"][-1:], "", "+"+p["size"], "w"], disk)

                # If there is one partition on the disk, we do not need to pass
                # a number to fdisk
                if (i != 0):
                    self.fdisk(["t", p["part"][-1:], types[p["flag"]], "w"], disk)
                else:
                    self.fdisk(["t", types[p["flag"]], "w"], disk)
                i = i + 1
        return 0

    # Function that call the disk binary with options for the console
    # lst is a list of option
    # disk is the physical disk for changes. (/dev/sda like)
    def     fdisk(self, lst, disk):
        args = "" # Argument string

        # List the arguments, concat them into a string
        for s in lst:
            args += s + "\n"

        # Call the fdisk binary with the disk
        p = Popen(['fdisk', disk], stdout=PIPE, stdin=PIPE, stderr=STDOUT)

        # Pipe the argument, for console (We need to convert the input into
        # bytes for python3)
        out = p.communicate(input=bytes(args, "UTF-8"))[0]

    # Function that format partitions
    # ext2 for Boot, swap for swap, ext4 for everything else
    def     format(self):
        layout = self.conf_lst["partitionning.layout"] # Partition future layout
        disk = self.conf_lst["partitionning.disk"] # Disk used for partitionning

        for p in layout:
            if p["disk"] == disk and p["flag"] != "Grub":
                self.dlg.infobox("Formatting partition "+ p["part"]+ "...",
                width=50, height=3)
                # If it's a /boot partition
                if (p["flag"] == "Boot"):
                    self.exec(["mkfs", "-t", "ext2", p["part"]])
                # If it's swap
                elif (p["flag"] == "Swap"):
                    self.exec(["mkswap", p["part"]])
                # Everything else, except Grub partition, that does not need
                # formatting
                else:
                    self.exec(["mkfs", "-t", "ext4", p["part"]])

    # Function that call a binary, with argument
    # args is the list of bin + arguments (['ls', '-la'])
    # Note that this function automatically hide the output of the command.
    # Return the output of the command, bytes format
    def     exec(self, args):
        p = Popen(args, stdout=PIPE, stderr=STDOUT)
        out = p.communicate()[0]
        return out
