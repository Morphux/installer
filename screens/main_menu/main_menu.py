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
# main_menu.py
# Created: 14/11/2016
# By: Louis Solofrizzo <louis@morphux.org>
##

class   Main_Menu:

##
# Variables
##
    dlg = 0
    conf_lst = {}
    a_title = "\nWelcome to the Morphux Installer\n\
For more information about the menu entries, See <Help> button";
    choices = [
        ("Install", "Launch system installation"),
        ("Custom Install", "Launch install from a configuration file"),
        ("Boot", "Just boot in the live CD"),
        ("Launch Shell", "Execute /bin/sh"),
        ("Options", "Open options screen"),
        ("Exit", "Quit this program (will reboot)")
    ]
    choices_ref = {
        "Install": {
            "t_id": 1,
            "help": "Launch the full, assisted, Morphux system installation"
        },
        "Custom Install": {
            "t_id": 0,
            "help": "Launch an automated install from a previous generated configuration file"
        },
        "Boot": {
            "t_id": 0,
            "help": "Enter the live-CD."
        },
        "Launch Shell": {
            "t_id": 0,
            "help": "Launch a basic shell. Advanced users only."
        },
        "Options": {
            "t_id": 0,
            "help": "Open the option screen"
        },
        "Exit": {
            "t_id": 0,
            "help": "Exit this program. This action will reboot the computer."
        }
    }

##
# Functions
##
    def     init(self, dialog, config_list):
        self.dlg = dialog
        self.conf_lst = config_list
        self.config = {
            "id": 0,
            "name": "Main Menu"
        }
        return self.config

    def     main(self):
        code, tag = self.dlg.menu(self.a_title, title="Main Menu", choices = self.choices, help_button=True)
        if (code == "ok" and tag == "Exit"):
            return -2
        elif (code == "help"):
            self.dlg.msgbox(self.choices_ref[tag]["help"])
            return 0
        elif (code == "cancel"):
            return -2
        else:
            return self.choices_ref[tag]["t_id"]

