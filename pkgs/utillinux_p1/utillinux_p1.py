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
# utillinux_p1.py
# Created: 09/12/2016
# By: Louis Solofrizzo <louis@morphux.org>
##

import      os

class   Utillinux_P1:

    conf_lst = {}
    e = False
    root_dir = ""

    def     init(self, c_lst, ex, root_dir):
        self.conf_lst = c_lst
        self.e = ex
        self.root_dir = root_dir
        self.config = {
            "name": "util-linux", # Name of the package
            "version": "2.28.1", # Version of the package
            "size": 114, # Size of the installed package (MB)
            "archive": "util-linux-2.28.1.tar.xz", # Archive name
            "SBU": 0.8, # SBU (Compilation time)
            "tmp_install": True, # Is this package part of the temporary install
            "next": "xz", # Next package to install
            "before": False,
            "after": False,
            "urls": [ # Url to download the package. The first one must be morphux servers
                "https://install.morphux.org/packages/util-linux-2.28.1.tar.xz"
            ]
        }
        return self.config

    def     configure(self):
        return self.e(["./configure",
                "--prefix=/tools",
                "--without-python",
                "--disable-makeinstall-chown",
                "--without-systemdsystemunitdir",
                "PKG_CONFIG=\"\""
        ], shell=True)

    def     make(self):
        return self.e(["make", "-j", self.conf_lst["cpus"]])

    def     install(self):
        return self.e(["make", "install"])
