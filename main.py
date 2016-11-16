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
    modules = {}
    d = Dialog(dialog="dialog",autowidgetsize=True)
    conf_lst = {}
    screens = []

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
        for d in lst:
            s = os.path.abspath(path) + os.sep + d
            if os.path.isdir(s) and os.path.exists(s + os.sep + "__init__.py"):
                dir.append(d)
        for d in dir:
            res[d] = __import__(path + "." + d + "." + d, fromlist = ["*"])
            res[d] = getattr(res[d], d.title())
        self.modules = res
        self.get_screens_infos()

    # Get infos on screens
    def     get_screens_infos(self):
        config = {}
        m_done = []
        for name, klass in self.modules.items():
            print("Reading "+ name +" module ...  ", end="")
            klass = klass()
            config = klass.init(self.d, self.conf_lst)
            self.screens.insert(config["id"], klass)
            print("Done !")

    def     main(self):
        nm = 0
        t_id = 0
        while 1:
            print(self.conf_lst)
            t_id = self.screens[nm].main()
            if (t_id == -2):
                return 0
            elif (t_id != nm):
                nm = t_id


main = Main()
