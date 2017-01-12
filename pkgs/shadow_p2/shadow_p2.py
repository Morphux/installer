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
# shadow_p2.py
# Created: 21/12/2016
# By: Louis Solofrizzo <louis@morphux.org>
##

import      os

class   Shadow_P2:

    conf_lst = {}
    e = False
    root_dir = ""

    def     init(self, c_lst, ex, root_dir):
        self.conf_lst = c_lst
        self.e = ex
        self.root_dir = root_dir
        self.config = {
            "name": "shadow", # Name of the package
            "version": "4.2.1", # Version of the package
            "size": 42, # Size of the installed package (MB)
            "archive": "shadow-4.2.1.tar.xz", # Archive name
            "SBU": 0.2, # SBU (Compilation time)
            "tmp_install": False, # Is this package part of the temporary install
            "next": "psmisc", # Next package to install
            "urls": [ # Url to download the package. The first one must be morphux servers
                "https://install.morphux.org/packages/shadow-4.2.1.tar.xz"
            ]
        }
        return self.config

    def     before(self):
        self.e(["sed -i 's/groups$(EXEEXT) //' src/Makefile.in"], shell=True)
        self.e(["find man -name Makefile.in -exec sed -i 's/groups\.1 / /' {} \;"], shell=True)
        self.e(["find man -name Makefile.in -exec sed -i 's/getspnam\.3 / /' {} \;"], shell=True)
        self.e(["find man -name Makefile.in -exec sed -i 's/passwd\.5 / /' {} \;"], shell=True)
        self.e(["sed -i -e 's@#ENCRYPT_METHOD DES@ENCRYPT_METHOD SHA512@' -e 's@/var/spool/mail@/var/mail@' etc/login.defs"], shell=True)
        return self.e(["sed -i 's/1000/999/' etc/useradd"], shell=True)

    def     configure(self):
        return self.e(["./configure",
                    "--sysconfdir=/etc",
                    "--with-group-name-max-length=32"
        ])

    def     make(self):
        return self.e(["make", "-j", self.conf_lst["cpus"]])

    def     install(self):
        return self.e(["make", "install"])

    def     after(self):
        if "MERGE_USR" in self.conf_lst["config"] and self.conf_lst["config"]["MERGE_USR"] != True:
            self.e(["mv", "-v", "/usr/bin/passwd", "/bin"])
        self.e(["pwconv"])
        return self.e(["grpconv"])
