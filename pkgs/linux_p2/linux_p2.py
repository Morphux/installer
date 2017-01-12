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
# linux_p2.py
# Created: 11/01/2017
# By: Louis Solofrizzo <louis@morphux.org>
##

import      os

class   Linux_P2:

    conf_lst = {}
    e = False
    root_dir = ""

    def     init(self, c_lst, ex, root_dir):
        self.conf_lst = c_lst
        self.e = ex
        self.root_dir = root_dir
        self.config = {
            "name": "linux", # Name of the package
            "version": "4.7.2", # Version of the package
            "size": 700, # Size of the installed package (MB)
            "archive": "linux-4.7.2.tar.xz", # Archive name
            "SBU": 6, # SBU (Compilation time)
            "tmp_install": False, # Is this package part of the temporary install
            "next": False, # Next package to install
            "urls": [ # Url to download the package. The first one must be morphux servers
                "https://install.morphux.org/packages/linux-4.7.2.tar.xz"
            ]
        }
        return self.config

    def     before(self):
        return self.e(["make", "mrproper"])

    def     configure(self):
        return self.e(["make", "defconfig"])

    def     make(self):
        return self.e(["make", "-j", self.conf_lst["cpus"]])

    def     install(self):
        x86_archs = ["x86_64", "x86_32", "i686", "i386"]

        if self.conf_lst["arch"] in x86_archs:
            self.e(["cp", "-v", "arch/x86/boot/bzImage", "/boot/vmlinuz-4.7.2-morphux"])
        self.e(["cp", "-v", "System.map", "/boot/System.map-4.7.2"])
        return self.e(["cp", "-v", ".config", "/boot/config-4.7.2"])

    def     after(self):
        self.e(["make", "modules_install"])
        self.e(["cp", "-rfv", "../linux-4.7.2", "/usr/src/linux-4.7.2"])
        return self.e(["ln", "-sv", "/usr/src/linux-4.7.2", "/usr/src/linux-current"])
