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

class   Conf_Install:

##
# Variables
##

    dlg = 0
    conf_lst = {}

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
        return self.config

    def     main(self):
        if (self.hostname()):
            return 0
        if (self.root_password()):
            return 0
        return 2

    def     hostname(self):
        string = ""
        while string == "":
            code, string = self.dlg.inputbox("Please enter your hostname:")
            if (string == "" and code != "cancel"):
                self.dlg.msgbox("Cannot be blank")
            elif (code == "cancel"):
                return 1
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
        return 0
