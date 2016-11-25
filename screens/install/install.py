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
