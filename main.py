#! /usr/bin/env python3
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
# main.py
# Created: 14/11/2016
# By: Louis Solofrizzo <louis@morphux.org>
##

import locale
from pythondialog.dialog import *
import time

##
# Global configuration
##
title = "Morphux Installer"
version = "1.0"

class   Main:

##
# Variables
##
    modules = {} # Object used to list modules
    # Dialog instance. autowidgetsize=True is just for autosizing the dialog boxes
    d = Dialog(dialog="dialog",autowidgetsize=True)
    conf_lst = {} # Configuration object. This object is used for generating a configuration file
    screens = {} # Modules instances. Those instances are initialized.

##
# Functions
##
    # Construct function
    def     __init__(self):
        self.load_screens()
        locale.setlocale(locale.LC_ALL, '')
        self.d.set_background_title(title + ", version " + version)
        self.main()


    # Load differents modules in the path screens/
    def     load_screens(self, path = "screens"):
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
        self.get_screens_infos()

    # Get infos on screens, Initialize the instances
    def     get_screens_infos(self):
        config = {}
        m_done = []
        for name, klass in self.modules.items():
            print("Reading "+ name +" module ...  ", end="")
            klass = klass()
            # Calling the init() function of each module
            config = klass.init(self.d, self.conf_lst)
            # Stocking the return of init() in an object
            self.screens[config["id"]] = [klass, config]
            print("Done !")

    # Main loop function
    def     main(self):
        nm = 0
        t_id = 0
        while 1:
            print(self.conf_lst)
            print(self.screens)
            t_id = self.screens[nm][0].main()
            # If the function return -2, a really bad things happened
            if (t_id == -2):
                return 0
            # The instance has done his job, switching to another screen
            elif (t_id != nm):
                nm = t_id


main = Main()
