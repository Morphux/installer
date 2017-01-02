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
# binutils2_p1.py
# Created: 04/12/2016
# By: Louis Solofrizzo <louis@morphux.org>
##

import      os

class   Binutils2_P1:

    conf_lst = {}
    e = False
    root_dir = ""

    def     init(self, c_lst, ex, root_dir):
        self.conf_lst = c_lst
        self.e = ex
        self.root_dir = root_dir
        self.config = {
            "name": "binutils2", # Name of the package
            "version": "2.27", # Version of the package
            "size": 533, # Size of the installed package (MB)
            "archive": "binutils-2.27.tar.bz2", # Archive name
            "SBU": 1.1, # SBU (Compilation time)
            "tmp_install": True, # Is this package part of the temporary install
            "next": "gcc2", # Next package to install
            "chdir": False,
            "urls": [ # Url to download the package. The first one must be morphux servers
                "https://install.morphux.org/packages/binutils-2.27.tar.bz2"
            ]
        }
        return self.config

    def     before(self):
        os.chdir("binutils-2.27")
        res = self.e(["rm", "-rf", "build"])
        res = self.e(["mkdir", "-vp", "build"])
        os.chdir("build")
        return res

    def     configure(self):
        os.environ["CC"] = self.conf_lst["target"] + "-gcc"
        os.environ["AR"] = self.conf_lst["target"] + "-ar"
        os.environ["RANLIB"] = self.conf_lst["target"] + "-ranlib"
        return self.e(["../configure",
                "--prefix=/tools",
                "--disable-nls",
                "--disable-werror",
                "--with-lib-path=/tools/lib",
                "--with-sysroot"
            ])

    def     make(self):
        return self.e(["make", "-j", self.conf_lst["cpus"]])

    def     install(self):
        return self.e(["make", "install"])

    def     after(self):
        self.e(["make", "-C", "ld", "clean"])
        self.e(["make", "-C", "ld", "LIB_PATH=/usr/lib:/lib"], shell=True)
        return self.e(["cp", "-v", "ld/ld-new", "/tools/bin"])
