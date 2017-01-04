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
# procpsng_p2.py
# Created: 21/12/2016
# By: Louis Solofrizzo <louis@morphux.org>
##

import      os

class   Procpsng_P2:

    conf_lst = {}
    e = False
    root_dir = ""

    def     init(self, c_lst, ex, root_dir):
        self.conf_lst = c_lst
        self.e = ex
        self.root_dir = root_dir
        self.config = {
            "name": "procps-ng", # Name of the package
            "version": "3.3.12", # Version of the package
            "size": 14, # Size of the installed package (MB)
            "archive": "procps-ng-3.3.12.tar.xz", # Archive name
            "SBU": 0.1, # SBU (Compilation time)
            "tmp_install": False, # Is this package part of the temporary install
            "next": "e2fsprogs", # Next package to install
            "after": False,
            "before": False,
            "urls": [ # Url to download the package. The first one must be morphux servers
                "https://install.morphux.org/packages/procps-ng-3.3.12.tar.xz"
            ]
        }
        return self.config

    def     configure(self):
        return self.e(["./configure",
                "--prefix=/usr",
                "--disable-static",
                "--exec-prefix=",
                "--libdir=/usr/lib",
                "--docdir=/usr/share/doc/procps-ng-3.3.12",
                "--disable-kill"
        ], shell=True)

    def     make(self):
        return self.e(["make", "-j", self.conf_lst["cpus"]])

    def     install(self):
        self.e(["make", "install"])
        self.e(["mv", "-v", "/usr/lib/libprocps.so.*", "/lib"], shell=True)
        return self.e(["ln -sfv ../../lib/$(readlink /usr/lib/libprocps.so) /usr/lib/libprocps.so"], shell=True)
