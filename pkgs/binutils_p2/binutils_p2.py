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
# binutils_p2.py
# Created: 14/12/2016
# By: Louis Solofrizzo <louis@morphux.org>
##

import      os

class   Binutils_P2:

    conf_lst = {}
    e = False
    root_dir = ""

    def     init(self, c_lst, ex, root_dir):
        self.conf_lst = c_lst
        self.e = ex
        self.root_dir = root_dir
        self.config = {
            "name": "binutils", # Name of the package
            "version": "2.27", # Version of the package
            "size": 488, # Size of the installed package (MB)
            "archive": "binutils-2.27.tar.bz2", # Archive name
            "SBU": 2.5, # SBU (Compilation time)
            "tmp_install": False, # Is this package part of the temporary install
            "next": False, # Next package to install
            "after": False,
            "urls": [ # Url to download the package. The first one must be morphux servers
                "https://install.morphux.org/packages/binutils-2.27.tar.bz2",
                "http://ftp.gnu.org/gnu/binutils/binutils-2.27.tar.bz2",
            ]
        }
        return self.config

    def     before(self):
        res = self.e(["mkdir", "-vp", "build"])
        os.chdir("build")
        return res

    def     configure(self):
        return self.e(["../configure",
                    "--prefix=/usr",
                    "--enable-shared",
                    "--disable-werror"
                ])

    def     make(self):
        return self.e(["make", "tooldir=/usr", "-j", self.conf_lst["cpus"]])

    def     install(self):
        return self.e(["make", "tooldir=/usr", "install"])
