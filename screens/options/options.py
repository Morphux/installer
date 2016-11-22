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
# options.py
# Created: 16/11/2016
# By: Louis Solofrizzo <louis@morphux.org>
##

class   Options:

##
# Variables
##

    dlg = 0 # Dialog Object
    conf_lst = {} # List object for configuration

    # Options used for the checklist. Format is:
    # (REAL_OPTION_NAME, English descripion, default)
    # default describe if the options is activated or not (boolean)
    # By default, the following options are activated:
    # MAKE_KERN, KEEP_SRC, BIN_INSTALL
    options = [
        ("INSTALL_DOC", "Install documentation when available", 0),
        ("KEEP_SRC", "Keep sources after compilation", 0),
        ("MAKE_KERN", "Compile Kernel", 1),
        ("KEEP_KSRC", "Keep Kernel sources", 1),
        ("BIN_INSTALL", "Install system with binaries only, do not compile anything (FASTER)", 1),
        ("LOG", "Log Install", 0),
        ("AUTO_REBOOT", "Reboot automatically after sucessfull install", 0),
        ("TMP_INSTALL", "Use a temporary system build (LFS-like, SLOWER)", 0),
        ("MERGE_USR", "Build the system with symbolic links between /{bin,sbin} and /usr", 1),
    ]

##
# Functions
##

    # Init function, called by Main instance
    def     init(self, dialog, config_list):
        self.dlg = dialog
        self.conf_lst = config_list
        self.config = {
            "id": 5,
            "name": "Options Menu"
        }

        # Fill the default options (in case the user never goes on this screen)
        res_opt = {}
        for i, opt in enumerate(self.options):
            if opt[2]:
                res_opt[opt[0]] = True
        self.conf_lst["config"] = res_opt
        return self.config

    # main function, called by Main instance
    def     main(self):
        res_opt = {}
        # Call the dialog checklist
        code, tag = self.dlg.checklist("Use Space to select options", choices = self.options, title="Options Menu")
        if code == "cancel":
            return 0

        # Empty the choices in the options
        for i, opt in enumerate(self.options):
            # Tuple can't handle writing on-the-fly
            # So we convert it into a list, make the change,
            # and convert it back into a tuple
            tmp = list(opt)
            tmp[2] = 0
            self.options[i] = tuple(tmp)
            # Empty the internal table too
            res_opt[tmp[0]] = False

        # Fill the chosen options in the list
        for s in tag:
            # This list is used for an internal use only
            # Format is list[REAL_OPTION_NAME] = True
            res_opt[s] = True
            for i, opt in enumerate(self.options):
                if opt[0] == s:
                    tmp = list(opt)
                    tmp[2] = 1
                    # We put the new tuple in place
                    self.options[i] = tuple(tmp)
        # Saving the options in the global configuration
        self.conf_lst["config"] = res_opt
        return 0
