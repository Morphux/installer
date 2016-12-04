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
# gcc2_p1.py
# Created: 04/12/2016
# By: Louis Solofrizzo <louis@morphux.org>
##

import      os

class   Gcc2_P1:

    conf_lst = {}
    e = False
    root_dir = ""

    def     init(self, c_lst, ex, root_dir):
        self.conf_lst = c_lst
        self.e = ex
        self.root_dir = root_dir
        self.config = {
            "name": "gcc2", # Name of the package
            "version": "6.2.0", # Version of the package
            "size": 533, # Size of the installed package (MB)
            "archive": "gcc-6.2.0.tar.bz2", # Archive name
            "SBU": 11, # SBU (Compilation time)
            "tmp_install": True, # Is this package part of the temporary install
            "next": False, # Next package to install
            "chdir": False,
            "urls": [ # Url to download the package. The first one must be morphux servers
                "https://install.morphux.org/packages/gcc-6.2.0.tar.bz2"
            ]
        }
        return self.config

    def     before(self):
        os.chdir("gcc-6.2.0")
        self.e(["rm", "-rf", "build"])
        self.e(["mkdir", "-vp", "build"])
        res = self.e(["cat", "gcc/limitx.h", "gcc/glimits.h", "gcc/limity.h",
                    ">", "`dirname $($LFS_TGT-gcc -print-libgcc-file-name)`/include-fixed/limits.h"], shell=True)
        os.chdir("build")
        return res

    def     configure(self):
        os.environ["CC"] = self.conf_lst["target"] + "-gcc"
        os.environ["CXX"] = self.conf_lst["target"] + "-g++"
        os.environ["AR"] = self.conf_lst["target"] + "-ar"
        return self.e(["../configure",
                "--prefix=/tools",
                "--with-local-prefix=/tools",
                "--with-native-system-header-dir=/tools/include",
                "--enable-languages=c,c++",
                "--disable-libstdcxx-pch",
                "--disable-multilib",
                "--disable-bootstrap",
                "--disable-libgomp"
            ])

    def     make(self):
        return self.e(["make", "-j", self.conf_lst["cpus"]])

    def     install(self):
        return self.e(["make", "install"])

    def     after(self):
        return self.e(["ln", "-sv", "gcc", "/tools/bin/cc"])
