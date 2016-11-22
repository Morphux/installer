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
# conf_install.py
# Created: 15/11/2016
# By: Louis Solofrizzo <louis@morphux.org>
##

import subprocess

class   Conf_Install:

##
# Variables
##

    dlg = 0 # Dialog Object
    conf_lst = {} # List object for configuration
    users_l = [] # List of users, used internally
    disks = {} # Disk and partitions object

##
# Functions
##

    # Init function, called by Main instance
    def     init(self, dialog, config_list):
        self.dlg = dialog
        self.conf_lst = config_list
        self.config = {
            "id": 1,
            "name": "Installation"
        }

        # Object containing each step of the configuration
        # This list is used to generate a menu, and for functions callbacks
        self.inst_step = [
            {"Hostname": [self.hostname, "Set machine hostname"]},
            {"Root password": [self.root_password, "Set root password"]},
            {"Users": [self.users, "Setup users account"]},
            {"Networking": [self.network, "Configure Networking"]},
            {"Partitionning": [self.partitionning, "Configure Partitionning for the Installation"]},
            {"Abort": [False, "Return to menu, reset configuration"]}
        ]
        return self.config

    # main function, called by Main instance
    def     main(self):
        # Since hostname is the first configuration to do, if the user
        # hit 'cancel' we return him to the Main Menu, not the step-by-step
        if (self.hostname()):
            return 0

        # If root_password returns 1, then the user hit cancel, and we
        # redirect him to the step-by-step menu
        if (self.root_password()):
            return self.step_by_step()

        # User accounts other than root are optionnal
        code = self.dlg.yesno("Do you want to setup other user accounts now ?")
        if code == "ok":
            if (self.users()):
                return self.step_by_step()

        if (self.network()):
            return self.step_by_step()

        if (self.partitionning()):
            return self.step_by_step()
        return 2

    # Step by Step configuration
    def     step_by_step(self):
        choices = [] # Menu choices list
        # Fill the choices automatically with the inst_step object
        for c in self.inst_step:
            for k, v in c.items():
                choices.append((k, v[1]))

        # Displaying the actual menu
        code, tag = self.dlg.menu("Choose a step in the installation", choices=choices, title="Step by Step")

        # If the choice is not abort, call the function, then recall the step_by_step function
        if (tag != "Abort" and code != "cancel"):
            for c in self.inst_step:
                for k, v in c.items():
                    if k == tag:
                        v[0]()
                        return self.step_by_step()

        # User press Abort, we empty the configuration, then return to the main menu
        else:
            self.conf_lst = {}
            return 0

    # Hostname handling function
    def     hostname(self):
        string = ""
        while string == "":
            # Input box for the hostname
            code, string = self.dlg.inputbox("Please enter your hostname:")

            # If the string is empty
            if (string == "" and code != "cancel"):
                self.dlg.msgbox("Cannot be blank")

            # If the user hit cancel
            elif (code == "cancel"):
                return 1

        # Register the hostname to the main config, then return to the main function
        self.conf_lst["system.hostname"] = string
        return 0

    # Root password handling function
    def     root_password(self):
        string = ""
        pass1 = ""

        while string == "":
            # Input box for the password
            # The insecure=True parameter is used for displaying stars instead of nothing at all
            code, string = self.dlg.passwordbox("Please enter you root password:", insecure=True)

            # If the password is empty
            if (string == "" and code != "cancel"):
                self.dlg.msgbox("Cannot be blank")

            # If the user hit cancel
            elif (code == "cancel"):
                return 1

        # Saving the first password in a tmp
        pass1 = string
        string = ""
        while string == "":
            # Input box for the password
            # The insecure=True parameter is used for displaying stars instead of nothing at all
            code, string = self.dlg.passwordbox("Please re-enter you root password:", insecure=True)

            # If the password is empty
            if (string == "" and code != "cancel"):
                self.dlg.msgbox("Cannot be blank")
            
            # If the user hit cancel
            elif (code == "cancel"):
                return 1

        # Compare the two passwords. If they did not match, we show a msgbox, then recall this very function
        if (pass1 != string):
                self.dlg.msgbox("Passwords do not match.")
                return self.root_password()

        # All good, saving the password, then return to the main function
        self.conf_lst["system.root_p"] = string
        return 0

    # Users configuration function. This function handle the menu, NOT the creation / editing
    # For that, see add_new_user
    def     users(self):
        while 1:
            # Choices by default, for the menu
            choices = [("Save", "Save the users and resume the installation"), ("New User", "Add a new user in the system")]

            # Test if we got any users to display
            if len(self.users_l):
                # Filling the choices table with entry to edit existing users
                for e in self.users_l:
                    choices.append((e["username"], "Edit "+ e["username"] + " account"));

            # Display the menu
            code, tag = self.dlg.menu("Edit / Add Users", title="Users Settings", choices=choices)

            # Save the users, return to the main function
            if (code == "ok" and tag == "Save"):
                self.conf_lst["system.users"] = self.users_l
                return 0

            # Creation of a new user
            if (code == "ok" and tag == "New User"):
                self.add_new_user()

            # User hit cancel
            elif (code == "cancel"):
                return 1

            # Editing existing user
            elif (code == "ok"):
                self.add_new_user(tag)

    # User add / edit function.
    # The user parameter is used to determine if we creating a user, or editing one
    # Of course, the username passed must exist in users_l
    def     add_new_user(self, user = ""):
        # Default value for the fields
        list = ["", "", "/bin/false", "/home/$USER"]

        # If the user parameter exist, we try to find the existing user in users_l
        if (user != ""):
            for o in self.users_l:
                # We found the user, no we replacing the default values by the actual ones
                if o["username"] == user:
                    list = [o["username"], o["groups"], o["shell"], o["home"]]

        while list[0] == "" or user != "":

            # Display the actual form
            # The first parameter is the header above the form
            # The second parameter is a list of tuple, with a format like this:
            # (label, yl, xl, item, yi, xi, field_length, input_length)
            code, list = self.dlg.form("Please provide the following informations:", [
                ("Username", 1, 1, list[0], 1, 20, 30, 30),
                ("Groups", 2, 1, list[1], 2, 20, 30, 30),
                ("Default shell", 3, 1, list[2], 3, 20, 30, 30),
                ("Home directory", 4, 1, list[3], 4, 20, 30, 30),
            ])

            # User hit cancel
            if (code == "cancel"):
                return 1

            # Checking if the username is empty
            if (list[0] == ""):
                # If it is, we print a message, the recall this function
                self.dlg.msgbox("Username cannot be blank")
                return self.add_new_user()

            # Check if the asked username exist already
            # Note: We are not checking in /etc/passwd or any user database in Unix,
            # just our current users array
            if user == "" or user != list[0]:
                for o in self.users_l:
                    if (o["username"] == list[0]):
                        # If the user was found, we print a message, then recall this function
                        self.dlg.msgbox("Username '"+ list[0] +"' already exist.")
                        return self.add_new_user(user)

            # Call the two-step password setting for this user
            password = self.add_new_user_password(list[0])

            # In case the user hit cancel in the password asking,
            # the function will return an integer, not a string
            if (type(password) == type(1)):
                return 1

            # If the user is a new one, we create an entry in the users_l list
            if user == "":
                self.users_l.append({
                    "username": list[0],
                    "groups": list[1],
                    "shell": list[2],
                    "home": list[3],
                    "passw": password
               })

            # The user already exist, we update the entry
            else:
                for o in self.users_l:
                    if o["username"] == user:
                        self.users_l.remove(o)
                        self.users_l.append({
                            "username": list[0],
                            "groups": list[1],
                            "shell": list[2],
                            "home": list[3],
                            "passw": password
                        })
                user = ""

        return 0

    # User two-step password handling function
    # The second parameter, username, is a string containing the username
    # Is just used to print title
    def     add_new_user_password(self, username):
        string = ""
        pass1 = ""

        while string == "":
            # Input box for the password
            # The insecure=True parameter is used for displaying stars instead of nothing at all
            code, string = self.dlg.passwordbox("Please enter "+ username +" password's:", insecure=True)

            # If the password is empty
            if (string == "" and code != "cancel"):
                self.dlg.msgbox("Cannot be blank")

            # If the user hit cancel
            elif (code == "cancel"):
                return 1

        # Saving the first password in a tmp
        pass1 = string
        string = ""
        while string == "":
            # Input box for the password
            # The insecure=True parameter is used for displaying stars instead of nothing at all
            code, string = self.dlg.passwordbox("Please re-enter the password:", insecure=True)

            # If the password is empty
            if (string == "" and code != "cancel"):
                self.dlg.msgbox("Cannot be blank")

            # If the user hit cancel
            elif (code == "cancel"):
                return 1

        # Compare the two passwords. If they did not match, we show a msgbox, then recall this very function
        if (pass1 != string):
                self.dlg.msgbox("Passwords do not match.")
                return self.add_new_user_password()

        # All good, returning the password
        return string

    # Network menu function handling
    def     network(self):
        # Choices for the menu
        choices = [("DHCP", "Automatically attribute IP address, no configuration to do"),
                    ("Manual", "Configure network manually"),
                    ("Pass", "Will not configure network for install")]

        # Actual display of the menu
        code, tag = self.dlg.menu("Choose your method for configuring networking.\nIf you don't know, choose DHCP.",
                        choices=choices, title="Configure Network")

        # If the user hit cancel
        if (code == "cancel"):
            return 1

        # If the user choose DHCP
        if (code == "ok" and tag == "DHCP"):
            self.conf_lst["network"] = "DHCP"
            return 0

        # If the user choose manual configuration
        if (code == "ok" and tag == "Manual"):
            return self.manual_networking()

        # If the user choose none of theses options, we print a yes / no question
        # in order to warn him about the consequences.
        if (code == "ok" and tag == "Pass"):

            code = self.dlg.yesno("Are you SURE ?\nNetwork will NOT be\
                configured for installation, additionnal packages will not be downloaded,\
                The installed system will be very minimal.");

            # If the user cancel his action, we recall this function
            if code == "cancel":
                return self.network()

            # User is sure, we stock the value, return to main
            self.conf_lst["network"] = "None"
        return 0

    # Manual networking handling function
    # The second parameter, list, is used to edit actual values,
    # rather than make new ones each time
    def     manual_networking(self, list = False):
        # If the second parameter don't exist, we fill the list with default choices
        if (type(list) == type(False)):
            list = ["", "255.255.255.255", "", "8.8.8.8,4.4.4.4"]

        # Actual display of the form
        # The first parameter is the header above the form
        # The second parameter is a list of tuple, with a format like this:
        # (label, yl, xl, item, yi, xi, field_length, input_length)
        code, list = self.dlg.form("Informations required:", [
            ("IP", 1, 1, list[0], 1, 20, 30, 30),
            ("Netmask", 2, 1, list[1], 2, 20, 30, 30),
            ("Gateway", 3, 1, list[2], 3, 20, 30, 30),
            ("DNS", 4, 1, list[3], 4, 20, 30, 30)
        ])

        # If the user hit cancel
        if (code == "cancel"):
            return 1

        # Check if all the fields are filled
        if (list[0] == "" or list[1] == "" or list[2] == "" or list[3] == ""):
            # If not, we print a message, then recall this function.
            self.dlg.msgbox("All fields must be filled.")
            return self.manual_networking(list)

        # All good, we save the configuration, then return to main
        self.conf_lst["network"] = {
            "IP": list[0],
            "NM": list[1],
            "GW": list[2],
            "DNS": list[3]
        }
        return 0

    # Partitionning handling function
    # This function _does not_ get the informations about the disks / partitions
    # See: get_partitions_info
    def     partitionning(self):
        # Choices for the menu
        choices = [
            ("Entire Disk", "Use entire disk for the system"),
            ("Entire Disk, Encrypted", "Use entire encrypted disk for the system"),
            ("Manual", "Manual configuration of the partitions (Advanced users only !)")
        ]

        # Execute fdisk, parse the result
        self.get_partitions_info()

        # Actual call to the menu display
        code, tag = self.dlg.menu("Choose a partitionning option", choices=choices, title="Partitionning")

        # If the user hit cancel, we return him to the step-by-step menu
        if code == "cancel":
            return 1

        # If the user choose entire disk option
        if tag == "Entire Disk":
            self.guided_partitionning()
        elif tag == "Entire Disk, Encrypted":
            self.guided_partitionning(1)
        elif tag == "Manual":
            self.manual_partitionning()

    # Disk / Partitions parsing function
    # This function _does not_ handle the partitionning menu, just the parsing
    # See: partitionning
    def     get_partitions_info(self):
        # Units used for parsing fdisk output
        # M = Mb, G = Gb, etc
        units = ["M", "G", "T", "P", "E", "Z", "Y"]
        i = 0

        # Execute fdisk -l command
        fdisk = subprocess.check_output(["fdisk", "-l"]).splitlines()
        #####
        # Example output of the fdisk -l command:
        #
        # Disk /dev/sda: 931.5 GiB, 1000204886016 bytes, 1953525168 sectors
        # Units: sectors of 1 * 512 = 512 bytes
        # Sector size (logical/physical): 512 bytes / 4096 bytes
        # I/O size (minimum/optimal): 4096 bytes / 4096 bytes
        # Disklabel type: dos
        # Disk identifier: 0xe47332bc
        # 
        # Device     Boot      Start        End    Sectors   Size Id Type
        # /dev/sda1  *          2048     206847     204800   100M  7 HPFS/NTFS/exFAT
        # /dev/sda2           206848 1245001727 1244794880 593.6G  7 HPFS/NTFS/exFAT
        # /dev/sda3       1245001728 1953523711  708521984 337.9G  5 Extended
        # /dev/sda5       1245003776 1945131007  700127232 333.9G 83 Linux
        # /dev/sda6       1945133056 1953523711    8390656     4G 82 Linux swap / Solaris
        # 
        # Disk /dev/sdb: 7.5 GiB, 8019509248 bytes, 15663104 sectors
        # Units: sectors of 1 * 512 = 512 bytes
        # Sector size (logical/physical): 512 bytes / 512 bytes
        # I/O size (minimum/optimal): 512 bytes / 512 bytes
        # Disklabel type: dos
        # Disk identifier: 0x2d031adc
        # 
        # Device     Boot  Start    End Sectors  Size Id Type
        # /dev/sdb1            0 542719  542720  265M  0 Empty
        # /dev/sdb2  *    526968 533231    6264  3.1M  1 FAT12
        #####

        # Iterating over each line of the result
        while i < len(fdisk):

            # Transform the line in a string, and remove the "b'" at the
            # beginning of the string
            s = str(fdisk[i])[2:]

            # If the line contain the disk info
            # Disk /dev/sda: 931.5 GiB, 1000204886016 bytes, 1953525168 sectors
            if s[:4] == "Disk":
                # We split the line over space
                infos = s.split(" ")

                # Set the basic informations about the disk
                self.disks[infos[1][:-1]] = {
                    "size": infos[2],
                    "unit": infos[3][:-1],
                    "part": []
                }

                # Iterate over the lines to the 'Disklabel' one
                while i < len(fdisk) and str(fdisk[i])[2:][:9] != "Disklabel":
                    print(str(fdisk[i])[2:][:9])
                    i = i + 1

                # We split the line in order to get the information
                # Disklabel type: dos
                label_infos = str(fdisk[i]).split(" ")

                # Let's check if the line is correct
                if (len(label_infos) >= 2):
                    # Stock the label information
                    self.disks[infos[1][:-1]]["label"] = label_infos[2][:-1]

                # Iterate over the lines to the 'Disk identifier' one
                # Disk identifier: 0x2d031adc
                while i < len(fdisk) and str(fdisk[i])[2:][:15] != "Disk identifier":
                    i = i + 1

                disk_name = str(fdisk[i]).split(" ")

                # Let's check if the line is correct
                if (len(disk_name) >= 2):
                    # Stock the label information
                    self.disks[infos[1][:-1]]["name"] = disk_name[2][:-1]

                # Iterate over the lines under the 'Disk' one
                while i < len(fdisk) and str(fdisk[i])[2:] != "'":
                    i = i + 1

                i = i + 1
                # Read information about the partitions
                while i < len(fdisk) and str(fdisk[i])[2:] != "'":

                    # Split the line in order to read it
                    d_part = str(fdisk[i])[2:].split()

                    # If it's not the 'Device ...' Line
                    if d_part[0] != "Device":

                        # Initialize the partition object
                        part_info = {}

                        # Get the partition name (/dev/sdX1 like)
                        part_info["part"] = d_part[0]

                        # If the partition marked as a boot one
                        if d_part[1] == "*":
                            part_info["boot"] = True
                        else:
                            part_info["boot"] = False
                        j = 2

                        # Iterate over the information, stop over the size column
                        while j < len(d_part) and d_part[j][-1:] not in units:
                            j = j + 1

                        # Get the size info (100M like)
                        part_info["size"] = d_part[j]

                        # Skip the id column, only on dos type disks
                        if (self.disks[infos[1][:-1]]["label"] == "dos"):
                            j = j + 2
                        else:
                            j = j + 1

                        type = ""
                        # Get the type of the partition
                        # Can be one word, or many, hence the while.
                        while j < len(d_part):
                            if j == len(d_part) - 1:
                                d_part[j] = d_part[j][:-1]
                            if type != "":
                                type += " " + d_part[j]
                            else:
                                type = d_part[j]
                            j = j + 1

                        # Add the type of the partition
                        part_info["type"] = type

                        # Add the partition object to the disk one
                        self.disks[infos[1][:-1]]["part"].append(part_info)
                    i = i + 1
            i = i + 1

    # Guided Partitionning handling Function
    # Note: Guided Partitionning is called 'Use an entire disk' in the installer
    def     guided_partitionning(self, encrypted = 0):
        # Choices for the menu
        choices = []

        # Fill the menu choices with disk informations
        for k, d in self.disks.items():
            choices.append((k, "Use the disk "+ k +" for the system ("+ d["size"] + d["unit"] +")"))

        # Actual call to the menu
        code, tag = self.dlg.menu("Choose a disk", choices=choices, title="Partitionning")

        # If the user hit the 'cancel' button
        if code == "cancel":
            return self.partitionning()

        # If the choosen disk has partitions, we warn the user
        if len(self.disks[tag]["part"]):
            code = self.dlg.yesno("This disk already have partitions.\n\
They will be totally wiped with the install.\n\
YOU WILL LOOSE ANY DATA THAT'S ON THE DISK.\n\
Are you sure to continue?")
            # If the user hit 'No', we recall this very function
            if code == "cancel":
                self.guided_partitionning(encrypted)

        # Save the choosen disk
        self.conf_lst["partitionning.disk"] = tag

        # Choices for guided partitionning
        choices = [
            ("Three partitions", "Root, boot and swap partitions. Strongly advised for unexperienced users."),
            ("Four partitions", "Root, boot, /home and swap partitions"),
            ("Five partitions", "Root, boot, /home, /tmp and swap partitions")
        ]

        # Actual call to the menu
        code, tag = self.dlg.menu("Choose a partitionning method:", choices=choices, title="Partitionning")

        # If the user hit cancel, we recall this function.
        if code == "cancel":
            self.guided_partitionning(encrypted)

    # Manual Partitionning function handler
    # Note: This function does not any change to the disk
    def     manual_partitionning(self):
        # Choices list
        choices = []

        # Fill the choices list with disks and partitions
        for k, d in self.disks.items():
            # Disk top line
            choices.append(("", "|-------------------------------------------------------"))

            choices.append((k, "| "+ k.replace("/dev/", "") +": "+ d["name"] +" "+ d["size"] + d["unit"] + " (" + d["label"] +")"))
            i = 0
            # Size used, in MB
            size_used = 0
            in_extended = 0

            # If the disk contain any partition, we shom a column helper
            if len(d["part"]):
                choices.append(("", "|   ID Name\t\tBoot\tSize\tType"))
                choices.append(("", "|   ========================================"))
            for p in d["part"]:
                # If the partition type is Extended, we don't wanna count it
                if p["type"] != "Extended":
                    size_used += self.size_to_mb(float(p["size"][:-1]), p["size"][-1:])

                if in_extended == 0:
                    part_name = p["part"].replace("/dev/", "")
                else:
                    part_name = "└─ " + p["part"].replace("/dev/", "")
                if p["boot"]:
                    choices.append((p["part"], "|   "+ str(i) +"  "+ part_name +"\t\t*\t"+ p["size"] +"\t"+ p["type"]))
                else:
                    choices.append((p["part"], "|   "+ str(i) +"  "+ part_name +"\t\t\t"+ p["size"] +"\t"+ p["type"]))
                if p["type"] == "Extended":
                    in_extended = 1
                i = i + 1

            # Get the size of the disk, in MB
            disk_size = self.size_to_mb(d["size"], d["unit"])

            # If we got more than 100MB of free space (Less is very likely to be padding) we print it.
            if size_used - disk_size > 10:
                choices.append(("FS:"+k, "|      FREE SPACE\t\t"+ str(int(size_used) - int(disk_size)) + "M\tNone"))

        # Bottom line
        choices.append(("", "|-------------------------------------------------------"))

        # Actual call to the menu
        # Arguments:
        # no_tags=True, Do not display tags
        # extra_button=True, Activate extra button
        # extra_label="", Override the default label for the extra button
        code, tag = self.dlg.menu("Edit the partitions\nWARNING: The change will be applied at install, not here",
            choices=choices, title="Manual Partitionning", no_tags=True,
            extra_label="Edit", extra_button=True)

        # If the user hit cancel
        if code == "cancel":
            return 1
        # If the user hit the menu helper, we recall this very function
        elif tag == "":
            return self.manual_partitionning()
        # If the user press edit, launch the screen partition edit function, then recall this function
        elif code == "extra":
            self.part_edit(tag)
            return self.manual_partitionning()
        return 1

    def     part_edit(self, part_name):
        self.dlg.msgbox(part_name)
        return 0

    # Function that does the conversion from anything to MB
    def     size_to_mb(self, size, unit):
        # The size is already in MB
        if unit[0] == "M":
            return float(size)
        elif unit[0] == "G":
            return float(size) * 1024
        return 0
