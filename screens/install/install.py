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
import      shutil
from        urllib.request import urlretrieve
from        subprocess import Popen, PIPE, STDOUT, call
import      multiprocessing
from        pythondialog.dialog import *

class   Install:

##
# Variables
##

    dlg = 0 # Dialog object
    conf_lst = {} # List object for configuration
    modules = {} # Module object
    pkgs = {} # Packages instances
    mnt_point = "/mnt/morphux/" # Install mount point
    arch_dir = mnt_point + "/packages/" # Archive directory (Must end with a /)
    sums_url = "https://install.morphux.org/packages/CHECKSUMS" # checksums url
    sum_file = "CHECKSUMS"
    checksums = {} # Object of packages sums
    m_gauge = {} # Object used for easy progress install
    sbu_time = 0 # Standard Build Unit time
    total_sbus = 0 # Total SBU to install the system
    current_time = 0 # Current install time
    in_install = 0
    current_install = [] # Object used to save the installation progress
    def_install = mnt_point + "/.install" # Default path for the install progress file
    org_pwd = ""

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
        # Save the installer PWD
        self.org_pwd = os.getcwd()

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

        # If a pre-existing install is present, clean it
        if os.path.isdir(self.mnt_point):
            self.dlg.infobox("Cleaning "+ self.mnt_point +" repository...",
                width=50, height=3)
            self.exec(["umount", "-R", self.mnt_point], ignore=True)
            self.exec(["rm", "-rf", self.mnt_point], ignore=True)

        # If partitionning is needed, do it
        if "partitionning.disk.format" in self.conf_lst:
            self.create_partitions()

        # Format the partitions
        self.format()

        # Mount the partitions
        self.mount()

        self.pkg_download(self.pkgs)
        self.get_patches()

        # If the installation require a 2-Phase install
        if "BIN_INSTALL" not in self.conf_lst["config"] or \
            ("BIN_INSTALL" in self.conf_lst["config"] and self.conf_lst["config"]["BIN_INSTALL"] == False):
            # Create the tools directory
            self.exec(["mkdir", "-v", self.mnt_point + "/tools"])
            # Link between the host and the install
            self.exec(["ln", "-sv", self.mnt_point + "/tools", "/"])
            self.phase_1_install()
            self.mnt_kfs()
            os.chdir(self.org_pwd)
            self.skeleton(self.mnt_point)
            self.copy_files(self.mnt_point)
            self.chroot()
            self.links()
            self.phase_2_install()

        if "KEEP_SRC" not in self.conf_lst["config"] or \
            ("KEEP_SRC" in self.conf_lst["config"] and self.conf_lst["config"]["KEEP_SRC"] == False):
            self.clean_all()
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
            if config["tmp_install"]:
                self.pkgs[config["name"]] = [klass, config]
            else:
                self.pkgs[config["name"] + "_phase_2"] = [klass, config]
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
                    self.exec(["mkswap", p["part"]], ignore=True)
                # Everything else, except Grub partition, that does not need
                # formatting
                else:
                    self.exec(["mkfs", "-t", "ext4", p["part"]])

    # Function that call a binary, with argument
    # args is the list of bin + arguments (['ls', '-la'])
    # Note that this function automatically hide the output of the command.
    # Return the output of the command, bytes format
    def     exec(self, args, input=False, shell=False, ignore=False):
        if shell == True:
            p = Popen(' '.join(args), stdin=PIPE, stdout=PIPE, stderr=STDOUT, shell=True, env=os.environ)
        else:
            p = Popen(args, stdin=PIPE, stdout=PIPE, stderr=STDOUT, env=os.environ)
        if input != False:
            out = p.communicate(input=input)[0]
        else:
            out = p.communicate()[0]

        # Comment the following condition to turn off strict debug
        if p.returncode != 0 and ignore == False:
            tmp = self.in_install
            self.in_install = 0
            self.dlg.msgbox("ERROR in the command: "+ ' '.join(args) + "\nPress Enter too see log.")
            self.dlg.scrollbox(out.decode())
            # If we were in installation, resume the progress bar
            if tmp == 1:
                self.in_install = 1
                self.async_progress_bar()

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
                    self.exec(["/sbin/swapon", "-v", p["part"]], ignore=True)
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

        # Look for the phase 1 packages
        for name, pkg in self.pkgs.items():
            if pkg[1]["tmp_install"] == True:
                total_size += pkg[1]["size"]
                total_sbus += pkg[1]["SBU"]
                pkg_phase_1[name] = pkg

        self.inst_title = "Phase 1: Temporary Install"
        self.total_sbus = total_sbus
        self.current_time = time.time()

        # Change the PATH environment variable
        os.environ["PATH"] = "/tools/bin:" + os.environ["PATH"]
        self.in_install = 1
        self.install(pkg_phase_1, "binutils")
        self.in_install = 0
        self.clean_install(pkg_phase_1)

    # This function launch the phase-2 full installation
    def     phase_2_install(self):
        pkg_phase_2 = {}
        total_size = 0
        total_sbus = 0

        # Look for phase 2 package
        for name, pkg in self.pkgs.items():
            if pkg[1]["tmp_install"] == False:
                total_size += pkg[1]["size"]
                total_sbus += pkg[1]["SBU"]
                pkg_phase_2[pkg[1]["name"]] = pkg

        self.inst_title = "Phase 2: Installation"
        # Untar all the phase 2 packages
        self.untar_all(pkg_phase_2)
        # Change package directory
        self.arch_dir = "/packages";
        self.mnt_point = "/"
        self.total_sbus = total_sbus
        self.current_time = time.time()
        self.def_install = self.mnt_point + "/.install"
        self.in_install = 1
        self.install(pkg_phase_2, "linux-headers")
        self.in_install = 0

    # This function take an object of packages, check if the sources are there.
    # If they aren't, the function download them.
    def     pkg_download(self, pkg_list, untar=True):
        to_dl = [] # Package to download

        # If the archive directory is not here, we create it
        if os.path.isdir(self.arch_dir) == False:
            self.exec(["mkdir", "-vp", self.arch_dir])

        for name, pkg in pkg_list.items():
            # Archive is not here, we need to download it.
            if type(pkg[1]["archive"]) != type(False) and os.path.isfile(self.arch_dir + pkg[1]["archive"]) == False:
                to_dl.append(pkg[1])

        # If we got any package to download, download them.
        if len(to_dl):
            self.archive_dowload(to_dl)
        self.check_archive(pkg_list)
        if untar:
            self.untar_all(pkg_list)

    # Function that untar all the archives
    # lst is an object of the packages to decompress
    def     untar_all(self, lst):
        to_unpack = len(lst) # Number of package to untar
        unpacked = 1 # Current archives decompressed
        arch_done = [] # List of archives decompressed

        # Start the progress bar
        self.dlg.gauge_start("Unpacking "+ str(to_unpack) +" packages ...", width=50)

        # Iterating over the packages
        for name, p in lst.items():

            if type(p[1]["archive"]) == type(False):
                continue

            # Update the progress bar
            self.dlg.gauge_update(int((unpacked * 100) / to_unpack),
                "Unpacking "+ p[1]["archive"] + "...", True)

            # Some packages use the same sources, so we store the list
            # of already decompressed archives in order to not decompress
            # the same archive multiple times.
            if p[1]["archive"] not in arch_done:
                # Un-tar the archive
                self.untar(p[1])

                # Add the archive to the list
                arch_done.append(p[1]["archive"])

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
            if os.path.isfile(self.arch_dir + conf["archive"]) == False:
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

            if type(pkg[1]["archive"]) == type(False):
                continue

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
                self.sbu_time = (time.time() - start) * 1.5

            self.update_install_file(pkg[1])
            self.global_progress_bar(reset=True)
            if pkg[1]["next"] in lst:
                pkg = lst[pkg[1]["next"]]
            else:
                pkg = False
            installed += 1

        self.install = 0
        # Install is done, we removing the install progress file
        os.remove(self.def_install)
        return 0

    # This function take a package configuration, and untar an archive in
    # self.arch_dir directory, then chdir inside.
    def     untar(self, conf):
        # Chdir in the archives directory
        os.chdir(self.arch_dir)

        # Un-taring the archive
        if (os.path.isdir(conf["name"] + "-" + conf["version"])):
            return 1
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

    # This function update the install file (.install) by default
    # If an install fail, or is quitted, we can resume it later
    def     update_install_file(self, conf):
        # Update the object
        self.current_install.append(conf)

        # Open the install file
        with open(self.def_install, "w") as fd:
            # Dump the current install progress
            json.dump({"conf": self.conf_lst, "installed":
                self.current_install}, fd)

    # Function that chroot into the temporary install
    def     chroot(self):
        self.dlg.infobox("Chrooting...")
        os.chroot(self.mnt_point)
        os.environ["PATH"] = "/bin:/usr/bin:/usr/sbin:/tools/bin"
        self.dlg = Dialog(dialog="/tools/bin/dialog", autowidgetsize=True)
        self.dlg.set_background_title("Morphux Installer" + ", version " + "1.0")

    # Function that create the basic distribution skeleton
    def     skeleton(self, path = "/"):
        self.dlg.infobox("Creating skeleton...")
        self.exec(["mkdir", "-pv",
                    path + "{bin,boot,etc/{opt,sysconfig},home,lib/firmware,mnt,opt}"
        ], shell=True)
        self.exec(["mkdir", "-pv",
                    path + "{media/{floppy,cdrom},sbin,srv,var}"
        ], shell=True)
        self.exec(["install", "-dv", "-m", "0750", path + "root"])
        self.exec(["install", "-dv", "-m", "1777", path + "tmp", path + "var/tmp"])
        self.exec(["mkdir", "-pv",
                    path + "usr/{,local/}{bin,include,lib,sbin,src}"
        ], shell=True)
        self.exec(["mkdir", "-pv",
                    path + "usr/{,local/}share/{color,dict,doc,info,locale,man}"
        ], shell=True)
        self.exec(["mkdir", "-pv",
                    path + "usr/{,local/}share/{misc,terminfo,zoneinfo}"
        ], shell=True)
        self.exec(["mkdir", "-pv",
                    path + "usr/libexec"
        ], shell=True)
        self.exec(["mkdir", "-pv",
                    path + "usr/{,local/}share/man/man{1..8}"
        ], shell=True)

        if self.conf_lst["arch"] == "x86_64":
            self.exec(["ln", "-sv", "lib", path + "lib64"])
            self.exec(["ln", "-sv", "lib", path + "usr/lib64"])
            self.exec(["ln", "-sv", "lib", path + "usr/local/lib64"])

        self.exec(["mkdir", "-v", path + "var/{log,mail,spool}"], shell=True)
        self.exec(["ln", "-sv", path + "run", path + "var/run"])
        self.exec(["ln", "-sv", path + "run/lock", path + "var/lock"])
        self.exec(["mkdir", "-pv",
                    path + "var/{opt,cache,lib/{color,misc,locate},local}"
        ], shell=True)
        self.exec(["mkdir", "-pv", path + "usr/local/games"])
        self.exec(["mkdir", "-pv", path + "usr/share/games"])

        if "MERGE_USR" in self.conf_lst["config"] and self.conf_lst["config"]["MERGE_USR"] == True:
            # Removing previously created directories
            self.exec(["rm", "-rf", path + "bin"])
            self.exec(["rm", "-rf", path + "sbin"])

            # Link directories
            self.exec(["ln", "-sv", "/usr/bin", path + "bin"])
            self.exec(["ln", "-sv", "/usr/sbin", path + "sbin"])

    # This function does links vital to compilation
    def     links(self):
        self.dlg.infobox("Linking files...")
        self.exec(["ln", "-sv", "/tools/bin/sh", "/bin/sh"])
        self.exec(["ln", "-sv", "/tools/bin/{bash,cat,echo,pwd,stty}", "/bin"], shell=True)
        self.exec(["ln", "-sv", "/tools/bin/perl", "/usr/bin"])
        self.exec(["ln", "-sv", "/tools/lib/libgcc_s.so{,.1}", "/usr/lib"], shell=True)
        self.exec(["ln", "-sv", "", "/tools/lib/libstdc++.so{,.6}", "/usr/lib"], shell=True)
        self.exec(["sed 's/tools/usr/' /tools/lib/libstdc++.la > /usr/lib/libstdc++.la"], shell=True)
        self.exec(["ln", "-sv", "/proc/self/mounts", "/etc/mtab"])

    # This function create basic files for login programs
    def     login_links(self, path = "/"):
        self.dlg.infobox("Linking files...")
        self.exec(["touch", path + "var/log/{btmp,lastlog,faillog,wtmp}"], shell=True)
        self.exec(["chgrp", "-v", "utmp", path + "var/log/lastlog"])
        self.exec(["chmod", "-v", "664", path + "var/log/lastlog"])
        self.exec(["chmod", "-v", "600", path + "var/log/btmp"])

    # This function copy specificied files in defaultfiles/ and install them
    # on the system
    def     copy_files(self, path = "/"):
        directory = "defaultfiles/"
        files = {
            ("passwd", "etc/passwd"),
            ("group", "etc/group"),
            ("nsswitch.conf", "etc/nsswitch.conf"),
            ("ld.so.conf", "etc/ld.so.conf"),
            ("syslog.conf", "etc/syslog.conf"),
            ("vimrc", "etc/vimrc"),
            ("motd", "etc/motd")
        }

        self.dlg.infobox("Creating defaultfiles...")
        for f in files:
            shutil.copyfile(directory + f[0], path + f[1])

    # This function mounts kernel file system on the future installation
    # /dev, /proc, /sys, /run
    def     mnt_kfs(self):
        self.dlg.infobox("Mounting kernel file systems")
        self.exec(["mkdir", "-pv", self.mnt_point + "/{dev,proc,sys,run}"], shell=True)
        self.exec(["mknod", "-m", "600", self.mnt_point + "/dev/console", "c", "5", "1"])
        self.exec(["mknod", "-m", "660", self.mnt_point + "/dev/null", "c", "1", "3"])
        self.exec(["mount", "-v", "--bind", "/dev", self.mnt_point + "/dev"])
        self.exec(["mount", "-vt", "devpts", "devpts", self.mnt_point + "/dev/pts", "-o", "gid=5,mode=620"])
        self.exec(["mount", "-vt", "proc", "proc", self.mnt_point + "/proc"])
        self.exec(["mount", "-vt", "sysfs", "sysfs", self.mnt_point + "/sys"])
        self.exec(["mount", "-vt", "tmpfs", "tmpfs", self.mnt_point + "/run"])

    # This function download all the needed patches, and the archives not 
    # specificied in package configuration
    def     get_patches(self):
        # Patch files
        files = [
            "bash-4.3.30-upstream_fixes-3.patch",
            "sysvinit-2.88dsf-consolidated-1.patch",
            "readline-6.3-upstream_fixes-3.patch",
            "kbd-2.0.3-backspace-1.patch",
            "glibc-2.24-fhs-1.patch",
            "bzip2-1.0.6-install_docs-1.patch",
            "coreutils-8.25-i18n-2.patch",
            "bc-1.06.95-memory_leak-1.patch"
        ]
        base_url = "https://install.morphux.org/patches/"
        patch_content = ""

        # Get all the patches
        self.dlg.infobox("Getting patches...")
        for f in files:
            urlretrieve(base_url + f, self.arch_dir + f)

        # Check integrity of the patches against sums
        self.dlg.infobox("Checking integrity of patches...")
        for f in files:
            with open(self.arch_dir + f, "rb") as fd:
                patch_content = fd.read()
            patch_sum = self.exec(["md5sum"], input=bytes(patch_content))[0].decode()
            patch_sum = patch_sum.split(" ")[0]
            if (patch_sum != self.checksums[f]):
                self.dlg.msgbox("The integrity of patch "+ f +" is wrong ! Aborting ...")
                sys.exit(1)

    # This function clean all the uncompressed install, sources, and patches
    def     clean_install(self, packages):
        self.dlg.infobox("Cleaning installation...")
        for name, pkg in packages.items():
            if type(pkg[1]["archive"]) == type(False):
                continue
            self.exec(["rm", "-rf", self.arch_dir + pkg[1]["name"] + "-" + pkg[1]["version"]])

    # This function clean all the installation traces
    def     clean_all(self):
        self.exec(["rm", "-rf", "/tools"])
        self.exec(["rm", "-rf", "/packages"])
