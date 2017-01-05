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
# sudo_p2.py
# Created: 05/01/2017
# By: Louis Solofrizzo <louis@morphux.org>
##

import      os

class   Sudo_P2:

    conf_lst = {}
    e = False
    root_dir = ""

    def     init(self, c_lst, ex, root_dir):
        self.conf_lst = c_lst
        self.e = ex
        self.root_dir = root_dir
        self.config = {
            "name": "sudo", # Name of the package", # Version of the package
            "version": "1.8.19p1", # Version of the package
            "size": 29, # Size of the installed package (MB)
            "archive": "sudo-1.8.19p1.tar.gz", # Archive name
            "SBU": 0.4, # SBU (Compilation time)
            "tmp_install": False, # Is this package part of the temporary install
            "next": False, # Next package to install
            "before": False,
            "urls": [ # Url to download the package. The first one must be morphux servers
                "https://install.morphux.org/packages/sudo-1.8.19p1.tar.gz"
            ]
        }
        return self.config

    def     configure(self):
        return self.e(["./configure",
                "--prefix=/usr",
                "--libexecdir=/usr/lib",
                "--with-secure-path",
                "--with-all-insults",
                "--with-env-editor",
                "--docdir=/usr/share/doc/sudo-1.8.19p",
                "--with-passprompt=\"[sudo] password for %p\""
        ])

    def     make(self):
        return self.e(["make", "-j", self.conf_lst["cpus"]])

    def     install(self):
        return self.e(["make", "install"])

    def     after(self):
        return self.e(["ln", "-sfv", "libsudo_util.so.0.0.0", "/usr/lib/sudo/libsudo_util.so.0"])
