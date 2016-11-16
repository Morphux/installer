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

import time

class   Conf_Install:

##
# Variables
##

    dlg = 0
    conf_lst = {}
    users_l = []
   
##
# Functions
##
    def     init(self, dialog, config_list):
        self.dlg = dialog
        self.conf_lst = config_list
        self.config = {
            "id": 1,
            "name": "Installation"
        }
        self.inst_step = [
            {"Hostname": [self.hostname, "Set machine hostname"]},
            {"Root password": [self.root_password, "Set root password"]},
            {"Users": [self.users, "Setup users account"]},
            {"Abort": [False, "Return to menu, reset configuration"]}
        ]
        return self.config

    def     main(self):
        if (self.hostname()):
            return 0
        if (self.root_password()):
            return self.step_by_step()
        code = self.dlg.yesno("Do you want to setup other user accounts now ?")
        if code == "ok":
            if (self.users()):
                return self.step_by_step()
        return 2

    def     step_by_step(self):
        choices = []
        for c in self.inst_step:
            for k, v in c.items():
                choices.append((k, v[1]))
        code, tag = self.dlg.menu("Choose a step in the installation", choices=choices, title="Step by Step")
        if (tag != "Abort" and code != "cancel"):
            for c in self.inst_step:
                for k, v in c.items():
                    if k == tag:
                        v[0]()
                        return self.step_by_step()
        else:
            return 0

    def     hostname(self):
        string = ""
        while string == "":
            code, string = self.dlg.inputbox("Please enter your hostname:")
            if (string == "" and code != "cancel"):
                self.dlg.msgbox("Cannot be blank")
            elif (code == "cancel"):
                return 1
        self.conf_lst["system.hostname"] = string
        return 0

    def     root_password(self):
        string = ""
        pass1 = ""
        while string == "":
            code, string = self.dlg.passwordbox("Please enter you root password:", insecure=True)
            if (string == "" and code != "cancel"):
                self.dlg.msgbox("Cannot be blank")
            elif (code == "cancel"):
                return 1
        pass1 = string
        string = ""
        while string == "":
            code, string = self.dlg.passwordbox("Please re-enter you root password:", insecure=True)
            if (string == "" and code != "cancel"):
                self.dlg.msgbox("Cannot be blank")
            elif (code == "cancel"):
                return 1
        if (pass1 != string):
                self.dlg.msgbox("Passwords do not match.")
                return self.root_password()
        self.conf_lst["system.root_p"] = string
        return 0

    def     users(self):
        while 1:
            choices = [("Save", "Save the users and resume the installation"), ("New User", "Add a new user in the system")]
            if len(self.users_l):
                for e in self.users_l:
                    choices.append((e["username"], "Edit "+ e["username"] + " account"));
            code, tag = self.dlg.menu("Edit / Add Users", title="Users Settings", choices=choices)
            if (code == "ok" and tag == "Save"):
                self.conf_lst["system.users"] = self.users_l
                return 0
            if (code == "ok" and tag == "New User"):
                self.add_new_user()
            elif (code == "cancel"):
                return 1
            elif (code == "ok"):
                self.add_new_user(tag)

    def     add_new_user(self, user = ""):
        list = ["", "", "/bin/false", "/home/$USER"]
        if (user != ""):
            for o in self.users_l:
                if o["username"] == user:
                    list = [o["username"], o["groups"], o["shell"], o["home"]]
        while list[0] == "" or user != "":
            code, list = self.dlg.form("Please provide the following informations:", [
                ("Username", 1, 1, list[0], 1, 20, 30, 30),
                ("Groups", 2, 1, list[1], 2, 20, 30, 30),
                ("Default shell", 3, 1, list[2], 3, 20, 30, 30),
                ("Home directory", 4, 1, list[3], 4, 20, 30, 30),
            ])
            if (code == "cancel"):
                return 1
            if (list[0] == ""):
                self.dlg.msgbox("Username cannot be blank")
                return self.add_new_user()
            if user == "" or user != list[0]:
                for o in self.users_l:
                    if (o["username"] == list[0]):
                        self.dlg.msgbox("Username '"+ list[0] +"' already exist.")
                        return self.add_new_user(user)
            password = self.add_new_user_password(list[0])
            if (type(password) == type(1)):
                return 1
            if user == "":
                self.users_l.append({
                    "username": list[0],
                    "groups": list[1],
                    "shell": list[2],
                    "home": list[3],
                    "passw": password
               })
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

    def     add_new_user_password(self, username):
        string = ""
        pass1 = ""
        while string == "":
            code, string = self.dlg.passwordbox("Please enter "+ username +" password's:", insecure=True)
            if (string == "" and code != "cancel"):
                self.dlg.msgbox("Cannot be blank")
            elif (code == "cancel"):
                return 1
        pass1 = string
        string = ""
        while string == "":
            code, string = self.dlg.passwordbox("Please re-enter the password:", insecure=True)
            if (string == "" and code != "cancel"):
                self.dlg.msgbox("Cannot be blank")
            elif (code == "cancel"):
                return 1
        if (pass1 != string):
                self.dlg.msgbox("Passwords do not match.")
                return self.add_new_user_password()
        return string
