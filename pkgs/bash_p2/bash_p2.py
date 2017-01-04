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
# bash_p2.py
# Created: 21/12/2016
# By: Louis Solofrizzo <louis@morphux.org>
##

import      os

class   Bash_P2:

    conf_lst = {}
    e = False
    root_dir = ""

    def     init(self, c_lst, ex, root_dir):
        self.conf_lst = c_lst
        self.e = ex
        self.root_dir = root_dir
        self.config = {
            "name": "bash", # Name of the package
            "version": "4.3.30", # Version of the package
            "size": 50, # Size of the installed package (MB)
            "archive": "bash-4.3.30.tar.gz", # Archive name
            "SBU": 1.8, # SBU (Compilation time)
            "tmp_install": False, # Is this package part of the temporary install
            "next": "bc", # Next package to install
            "urls": [ # Url to download the package. The first one must be morphux servers
                "https://install.morphux.org/packages/bash-4.3.30.tar.gz"
            ]
        }
        return self.config

    def     before(self):
        return self.e(["patch", "-Np1", "-i", "../bash-4.3.30-upstream_fixes-3.patch"])

    def     configure(self):
        return self.e(["./configure",
                "--prefix=/usr",
                "--without-bash-malloc",
                "--docdir=/usr/share/doc/bash-4.3.30",
                "--with-installed-readline"
            ])

    def     make(self):
        return self.e(["make", "-j", self.conf_lst["cpus"]])

    def     install(self):
        return self.e(["make", "install"])

    def     after(self):
        if "MERGE_USR" in self.conf_lst["config"] and self.conf_lst["config"]["MERGE_USR"] != True:
            return self.e(["mv", "-vf", "/usr/bin/bash", "/bin"])
        else:
            return "", 0
