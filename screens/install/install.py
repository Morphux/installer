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
import      sys
import      time
import      datetime
import      threading
from        urllib.request import urlretrieve
from        subprocess import Popen, PIPE, STDOUT, call
import      multiprocessing

class   Install:

##
# Variables
##

    dlg = 0 # Dialog object
    conf_lst = {} # List object for configuration
    modules = {} # Module object
    pkgs = {} # Packages instances
    mnt_point = "/mnt/morphux" # Install mount point
    arch_dir = "/opt/packages/" # Archive directory
    sums_url = "https://install.morphux.org/packages/CHECKSUMS" # checksums url
    sum_file = "CHECKSUMS"
    checksums = {} # Object of packages sums
    m_gauge = {} # Object used for easy progress install
    sbu_time = 0 # Standard Build Unit time
    total_sbus = 0 # Total SBU to install the system
    current_time = 0 # Current install time
    in_install = 0

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

        # Get target architecture
        self.conf_lst["arch"] = self.exec(["uname", "-m"])[0].decode().split("\n")[0]
        self.conf_lst["target"] = self.exec(["uname", "-m"])[0].decode().split("\n")[0] + "-morphux-linux-gnu"

        # Get number of CPUs
        self.conf_lst["cpus"] = str(multiprocessing.cpu_count())

        # Load packages files
        self.load_pkgs()
        #self.phase_1_install()
        #sys.exit(1)

        # If a pre-existing install is present, clean it
        if os.path.isdir(self.mnt_point):
            self.dlg.infobox("Cleaning "+ self.mnt_point +" repository...",
                width=50, height=3)
            self.exec(["umount", "-R", self.mnt_point])
            self.exec(["rm", "-rf", self.mnt_point])

        # If partitionning is needed, do it
        if "partitionning.disk.format" in self.conf_lst:
            self.create_partitions()

        # Format the partitions
        self.format()

        # Mount the partitions
        self.mount()

        # If the installation require a 2-Phase install
        if "TMP_INSTALL" in self.conf_lst["config"] and self.conf_lst["config"]["TMP_INSTALL"]:
            # Create the tools directory
            self.exec(["mkdir", "-v", self.mnt_point + "/tools"])
            # Link between the host and the install
            self.exec(["ln", "-sv", self.mnt_point + "/tools", "/"])
            self.phase_1_install()

        self.dlg.msgbox("The installation is finished. Hit 'Enter' to close this dialog and reboot.", title="Success !")
        # Need reboot here
        sys.exit(1)

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
            config = klass.init(self.conf_lst, self.exec, self.mnt_point)
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
                self.dlg.infobox("Creating partition "+ p["part"] +"...",
                    width=50, height=3)
                self.fdisk(["n", p["part"][-1:], "", "+"+p["size"], "w"], disk)

                # If there is one partition on the disk, we do not need to pass
                # a number to fdisk
                if (i != 0):
                    self.fdisk(["t", p["part"][-1:], types[p["flag"]], "w"], disk)
                else:
                    self.fdisk(["t", types[p["flag"]], "w"], disk)
                i = i + 1

        # Re-create partition table
        self.dlg.infobox("Re-creating partition table...", width=50, height=3)
        self.exec(["partprobe", disk])
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
    def     exec(self, args, input=False, shell=False):
        if shell == True:
            p = Popen(' '.join(args), stdin=PIPE, stdout=PIPE, stderr=STDOUT, shell=True)
        else:
            p = Popen(args, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
        if input != False:
            out = p.communicate(input=input)[0]
        else:
            out = p.communicate()[0]
        return out, p.returncode

    # Function that mount the partitions for install
    # self.mnt_point is used for the mount point.
    def     mount(self):
        layout = self.conf_lst["partitionning.layout"] # Partition layout
        disk = self.conf_lst["partitionning.disk"] # Disk used for mount

        # Create the mount point directory
        self.exec(["mkdir", "-pv", self.mnt_point])

        # Let's look for the root partition, in order to mount it
        root = [p for p in layout if p["flag"] == "Root"]
        # Mount the root partition
        self.dlg.infobox("Mounting root partition...", width=50, height=3)
        self.exec(["mount", "-v", "-t", "ext4", root[0]["part"], self.mnt_point])

        # Mount all the others partition that needs mounting
        for p in layout:
            if p["flag"] != "Root" and p["flag"] != "Grub":
                # No need to mount anything for swap, just activate it
                self.dlg.infobox("Mounting "+ p["flag"]+ " partition...",
                width=50, height=3)
                if p["flag"] == "Swap":
                    self.exec(["/sbin/swapon", "-v", p["part"]])
                elif p["flag"] == "Boot":
                    # Create the directory, then mount it
                    self.exec(["mkdir", "-pv", self.mnt_point + "/boot"])
                    self.exec(["mount", "-v", "-t", "ext2", p["part"], self.mnt_point + "/boot"])
                elif p["flag"] == "Home":
                    # Create the directory, then mount it
                    self.exec(["mkdir", "-pv", self.mnt_point + "/home"])
                    self.exec(["mount", "-v", "-t", "ext4", p["part"], self.mnt_point + "/home"])
                elif p["flag"] == "Tmp":
                    # Create the directory, then mount it
                    self.exec(["mkdir", "-pv", self.mnt_point + "/tmp"])
                    self.exec(["mount", "-v", "-t", "ext4", p["part"], self.mnt_point + "/tmp"])
        return 0

    # This function launch the phase-1 full installation
    def     phase_1_install(self):
        pkg_phase_1 = {} # List of package to install for phase 1
        total_size = 0 # Total size of the install
        total_sbus = 0 # Total time of the install, in SBUs

        for name, pkg in self.pkgs.items():
            if pkg[1]["tmp_install"] == True:
                total_size += pkg[1]["size"]
                total_sbus += pkg[1]["SBU"]
                pkg_phase_1[name] = pkg

        self.pkg_download(pkg_phase_1)
        self.inst_title = "Phase 1: Temporary Install"
        self.total_sbus = total_sbus
        self.current_time = time.time()
        self.in_install = 1
        self.install(pkg_phase_1, "binutils")
        self.in_install = 0

    # This function take an object of packages, check if the sources are there.
    # If they aren't, the function download them.
    def     pkg_download(self, pkg_list):
        to_dl = [] # Package to download

        # If the archive directory is not here, we create it
        if os.path.isdir(self.arch_dir) == False:
            self.exec(["mkdir", "-vp", self.arch_dir])

        for name, pkg in self.pkgs.items():
            # Archive is not here, we need to download it.
            if os.path.isfile(self.arch_dir + pkg[1]["archive"]) == False:
                to_dl.append(pkg[1])

        # If we got any package to download, download them.
        if len(to_dl):
            self.archive_dowload(to_dl)
        self.check_archive(pkg_list)
        self.untar_all(pkg_list)

    # Function that untar all the archives
    # lst is an object of the packages to decompress
    def     untar_all(self, lst):
        to_unpack = len(lst) # Number of package to untar
        unpacked = 1 # Current archives decompressed

        # Start the progress bar
        self.dlg.gauge_start("Unpacking "+ str(to_unpack) +" packages ...", width=50)

        # Iterating over the packages
        for name, p in lst.items():

            # Update the progress bar
            self.dlg.gauge_update(int((unpacked * 100) / to_unpack),
                "Unpacking "+ p[1]["archive"] + "...", True)

            # Un-tar the archive
            self.untar(p[1])
            unpacked += 1

        # Stopping the progress bar
        self.dlg.gauge_stop()

    # This function handle the downloading of archive
    # The lst is a list of package to download
    def     archive_dowload(self, lst):
        dl_len = len(lst) # Number of packages to download
        to_dl = 1 # Current archives downloaded

        # First call to the update screen
        self.dlg.gauge_start("Downloading "+ str(dl_len) +" packages ...", width=50)

        # Iterate over packages to download
        for conf in lst:
            dl_ok = 0
            i = 0
            if os.path.isfile(self.arch_dir + conf["archive"] == False):
                # Test multiples urls in case one fail
                # TODO: Handle exception from retrieving
                while dl_ok == 0:
                    # Update the progress bar
                    self.dlg.gauge_update(int((to_dl * 100) / dl_len),
                        "Getting "+ conf["archive"]+ "... ("+ str(to_dl) +"/"+
                        str(dl_len) +")", True)
                    urlretrieve(conf["urls"][i], self.arch_dir + conf["archive"])
                    i += 1
                    dl_ok = 1
            to_dl += 1
        # Stop the progress bar
        self.dlg.gauge_stop()

    # Function that check the checksums of the package
    # This function take one argument, an object of package to check
    def     check_archive(self, pkg_list):
        to_check = len(pkg_list) # Number of package to check
        checked = 1 # Numbers of package checked

        self.get_checksums()
        # Start the gauge
        self.dlg.gauge_start("Checking integrity of "+ str(to_check) +" packages ...",
            width=50)

        # Iterate over the packages to check
        for name, pkg in pkg_list.items():

            # Read the archive into string
            with open(self.arch_dir + pkg[1]["archive"], "rb") as fd:
                pkg_content = fd.read()

            # Get the sum of the archive
            arch_sum = self.exec(["md5sum"], input=bytes(pkg_content))[0].decode()
            arch_sum = arch_sum.split(" ")[0]

            # Checking the sum
            if arch_sum != self.checksums[pkg[1]["archive"]]:
                # The sum is wrong, we warn the user, and we abort
                self.dlg.msgbox("The integrity of package "+ pkg[1]["name"]+
                    " is wrong ! Aborting ...")
                sys.exit(1)

            # All good, we update the gauge
            self.dlg.gauge_update(int(checked * 100 / to_check))
            checked += 1

        # Stop the gauge
        self.dlg.gauge_stop()

    # This function parse the checksums file, and if the is not here,
    # get it from the install.morphux.org server
    def     get_checksums(self):
        # Test if the file is already there
        try:
            fd = open(self.sum_file, 'r')

        except IOError:
            # If not, we retrieve it from the server
            urlretrieve(self.sums_url, self.sum_file)
            fd = open(self.sum_file, 'r')

        # Getting the file content
        content = fd.readlines()

        # Iterating over each line
        for line in content:
            line = line.strip("\n").split(" ")
            self.checksums[line[1]] = line[0]


    # This function launch the install of packages in lst, by compilation
    # lst is an object of all the packages with the name in key and a list
    # in value. The list is format like: [config_object, class_object]
    # first is a string argument used to begin the install by a package.
    # Then, the next package is defined in config["next"]
    def     install(self, lst, first):
        pkg = [p for k, p in lst.items() if p[1]["name"] == first][0]
        to_install = len(lst) # Len of package to install
        installed = 1

        while pkg != False:
            # Return to the archive dir
            os.chdir(self.arch_dir)

            # Init the global progress bar
            self.global_progress_bar(text="Installing "+ pkg[1]["name"] +"-"+ pkg[1]["version"]+ "...",
                percent=int((installed * 100) / to_install),
                conf="N/A", comp="N/A",
                inst="N/A", post_comp="N/A", pre_comp="In Progress")

            # If the package is the first, we measure the time
            if self.sbu_time == 0 and first == pkg[1]["name"]:
                start = time.time()
                self.async_progress_bar()

            # Chdir into the decompressed directory (Must be in the format name-version)
            if "chdir" not in pkg[1]:
                os.chdir(pkg[1]["name"] + "-" + pkg[1]["version"])

            # Before instructions
            if "before" not in pkg[1]:
                res = pkg[0].before()
                if res[1] != 0:
                    self.inst_error(res)
                self.global_progress_bar(pre_comp="Done")
            else:
                self.global_progress_bar(pre_comp="Skipped")

            self.global_progress_bar(conf="In Progress")
            # ./configure instructions
            if "configure" not in pkg[1]:
                res = pkg[0].configure()
                if res[1] != 0:
                    self.inst_error(res)
                self.global_progress_bar(conf="Done")
            else:
                self.global_progress_bar(conf="Skipped")

            self.global_progress_bar(comp="In Progress")
            # make instructions
            if "make" not in pkg[1]:
                res = pkg[0].make()
                if res[1] != 0:
                    self.inst_error(res)
                self.global_progress_bar(comp="Done")
            else:
                self.global_progress_bar(comp="Skipped")

            self.global_progress_bar(inst="In Progress")
           # make install instructions
            if "install" not in pkg[1]:
                res = pkg[0].install()
                if res[1] != 0:
                    self.inst_error(res)
                self.global_progress_bar(inst="Done")
            else:
                self.global_progress_bar(inst="Skipped")

            self.global_progress_bar(post_comp="In Progress")
            # after instructions
            if "after" not in pkg[1]:
                res = pkg[0].after()
                if res[1] != 0:
                    self.inst_error(res)
                self.global_progress_bar(post_comp="Done")
            else:
                self.global_progress_bar(post_comp="Skipped")

            # If the package is first, we stock the total build time
            if self.sbu_time == 0 and first == pkg[1]["name"]:
                self.sbu_time = (time.time() - start)

            self.global_progress_bar(reset=True)
            if pkg[1]["next"] in lst:
                pkg = lst[pkg[1]["next"]]
            else:
                pkg = False
            installed += 1

        self.install = 0
        return 0

    # This function take a package configuration, and untar an archive in
    # self.arch_dir directory, then chdir inside.
    def     untar(self, conf):
        # Chdir in the archives directory
        os.chdir(self.arch_dir)

        # Un-taring the archive
        self.exec(["tar", "xf", conf["archive"]])

    # Function that display the global progress bar for an install
    def     global_progress_bar(self, text="", percent=-1,
                pre_comp="", conf="", comp="", inst="", post_comp="", reset=False):

        # Setting the text
        if text != "":
            self.m_gauge["text"] = text

        # Setting the percents
        if percent != -1:
            self.m_gauge["percent"] = percent

        # Setting the pre compilation status
        if pre_comp != "":
            self.m_gauge["pre_comp"] = pre_comp

        # Setting the configuration status
        if conf != "":
            self.m_gauge["conf"] = conf

        # Setting the compilation status
        if comp != "":
            self.m_gauge["comp"] = comp

        # Setting the installation status
        if inst != "":
            self.m_gauge["inst"] = inst

        # Setting the post compilation status
        if post_comp != "":
            self.m_gauge["post_comp"] = post_comp

        if reset != False:
            self.m_gauge = {}
            return 0

    # Asynchronous function, that display the bar
    # Called every one second
    def     async_progress_bar(self):
        if self.in_install == 1:

            # Add the estimated time
            if self.sbu_time == 0:
                s_time = "\nEstimated time of install: N/A\n"
            else:
                est_time = self.sbu_time * self.total_sbus
                s_time = "\nEstimated time of install: " + time.strftime("%H:%M:%S", time.gmtime(est_time)) + "\n"

            s_time += "Current installation time: " + time.strftime("%H:%M:%S", time.gmtime(time.time() - self.current_time))

            self.dlg.mixedgauge(self.m_gauge["text"] + s_time, percent=self.m_gauge["percent"],
                elements = [
                    ("Pre-Compilation", self.m_gauge["pre_comp"]),
                    ("Configuration", self.m_gauge["conf"]),
                    ("Compilation", self.m_gauge["comp"]),
                    ("Installation", self.m_gauge["inst"]),
                    ("Post-Compilation", self.m_gauge["post_comp"]),
                ], title=self.inst_title)

            threading.Timer(1, self.async_progress_bar).start()

    # Function that handle installation error
    # exec_return arg is a tuple of (string_out, return_code)
    def     inst_error(self, exec_return):
        # Stop the progress bar thread
        self.in_install = 0

        # Print a dialog to ask the user if we want to see the log
        code = self.dlg.yesno("An error happened during the installation :(\nReturn code: "+
            str(exec_return[1])+"\nDo you want to see the log file ?")

        # If user press 'Yes'
        if code == "ok":
            # Show the output of the command
            self.dlg.scrollbox(exec_return[0].decode())

        # Abort the installation
        sys.exit(1)
