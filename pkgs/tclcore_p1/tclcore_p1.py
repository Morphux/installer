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
# tclcore_p1.py
# Created: 08/12/2016
# By: Louis Solofrizzo <louis@morphux.org>
##

import      os

class   Tclcore_P1:

    conf_lst = {}
    e = False
    root_dir = ""

    def     init(self, c_lst, ex, root_dir):
        self.conf_lst = c_lst
        self.e = ex
        self.root_dir = root_dir
        self.config = {
            "name": "tcl-core", # Name of the package
            "version": "8.6.6", # Version of the package
            "size": 40, # Size of the installed package (MB)
            "archive": "tcl-core8.6.6-src.tar.gz", # Archive name
            "SBU": 0.4, # SBU (Compilation time)
            "tmp_install": True, # Is this package part of the temporary install
            "next": False, # Next package to install
            "urls": [ # Url to download the package. The first one must be morphux servers
                "https://install.morphux.org/packages/tcl-core8.6.6-src.tar.gz"
            ]
        }
        return self.config

    def     before(self):
        return os.chdir("unix")

    def     configure(self):
        return self.e(["./configure",
                "--prefix=/tools"
            ])

    def     make(self):
        return self.e(["make", "-j", self.conf_lst["cpus"]])

    def     install(self):
        self.e(["make", "install"])
        return self.e(["make", "install-private-headers"])

    def     after(self):
        self.e(["chmod", "-v", "u+w", "/tools/lib/libtcl8.6.so"])
        return self.e(["ln", "-sv", "tclsh8.6", "/tools/bin/tclsh"])
