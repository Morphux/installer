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
# bzip_p2.py
# Created: 16/12/2016
# By: Louis Solofrizzo <louis@morphux.org>
##

import      os

class   Bzip2_P2:

    conf_lst = {}
    e = False
    root_dir = ""

    def     init(self, c_lst, ex, root_dir):
        self.conf_lst = c_lst
        self.e = ex
        self.root_dir = root_dir
        self.config = {
            "name": "bzip2", # Name of the package
            "version": "1.0.6", # Version of the package
            "size": 4.9, # Size of the installed package (MB)
            "archive": "bzip2-1.0.6.tar.gz", # Archive name
            "SBU": 0.1, # SBU (Compilation time)
            "tmp_install": False, # Is this package part of the temporary install
            "next": "pkg-config", # Next package to install
            "urls": [ # Url to download the package. The first one must be morphux servers
                "https://install.morphux.org/packages/bzip2-1.0.6.tar.gz"
            ]
        }
        return self.config

    def     before(self):
        self.e(["patch", "-Np1", "-i", "../bzip2-1.0.6-install_docs-1.patch"])
        return self.e(["sed -i 's@(PREFIX)/man@(PREFIX)/share/man@g' Makefile"], shell=True)

    def     configure(self):
        self.e(["make", "-f", "Makefile-libbz2_so"])
        return self.e(["make", "clean"])

    def     make(self):
        return self.e(["make", "-j", self.conf_lst["cpus"]])

    def     install(self):
        return self.e(["make", "PREFIX=/usr", "install"])

    def     after(self):
        self.e(["cp", "-v", "bzip2-shared", "/bin/bzip2"])
        self.e(["cp", "-av", "libbz2.so.*", "/lib"], shell=True)
        self.e(["ln", "-sv", "../../lib/libbz2.so.1.0", "/usr/lib/libbz2.so"])
        if "MERGE_USR" in self.conf_lst["config"] and self.conf_lst["config"]["MERGE_USR"] != True:
            self.e(["rm", "-v", "/usr/bin/{bunzip2,bzcat,bzip2}"], shell=True, ignore=True)
            self.e(["ln", "-sv", "bzip2", "/bin/bunzip2"])
            return self.e(["ln", "-sv", "bzip2", "/bin/bzcat"])
