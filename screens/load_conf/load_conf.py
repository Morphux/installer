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
# load_conf.py
# Created: 16/11/2016
# By: Louis Solofrizzo <louis@morphux.org>
##

import      json

class   Load_Conf:

##
# Variables
##

    dlg = 0  # Dialog object
    conf_lst = {} # List object for configuration

##
# Functions
##

    # Init function, called by Main instance
    def     init(self, dialog, config_list):
        self.dlg = dialog
        self.conf_lst = config_list
        self.config = {
            "id": 2,
            "name": "Load Configuration File"
        }
        return self.config

    # main function, called by Main instance
    # The second parameter, d_path is the default starting path
    def     main(self, Main, d_path = "/"):

        # Call to the file selection dialog box
        code, path = self.dlg.fselect(d_path, height=20, width=60, title="Select the configuration file")

        # If user hit cancel
        if (code == "cancel"):
            return 0

        # Try to open the file
        try:
            fd = open(path, 'r')

        # We got an error, show a message, then recall this function
        except IOError:
            self.dlg.msgbox("The file "+ path +" cannot be found.")
            return self.main(path)

        with fd:
            # All good, we can read the file
            self.conf_lst = json.load(fd)

            # TODO catch exception on json.load

            # Ugly method in order to check conf integrity
            Main.screens[1][0].conf_lst = self.conf_lst
            if Main.screens[1][0].check_conf():
                self.conf_lst["load_conf"] = True
                Main.conf_lst = self.conf_lst
                return 6
            return Main.screens[1][0].step_by_step()
