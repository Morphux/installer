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
# glibc_p1.py
# Created: 01/12/2016
# By: Louis Solofrizzo <louis@morphux.org>
##

import      os

class   Glibc_P1:

    conf_lst = {}
    e = False
    root_dir = ""

    def     init(self, c_lst, ex, root_dir):
        self.conf_lst = c_lst
        self.e = ex
        self.root_dir = root_dir
        self.config = {
            "name": "glibc", # Name of the package
            "version": "2.24", # Version of the package
            "size": 666, # Size of the installed package (MB)
            "archive": "glibc-2.24.tar.xz", # Archive name
            "SBU": 4, # SBU (Compilation time)
            "tmp_install": True, # Is this package part of the temporary install
            "after": False,
            "next": False, # Next package to install
            "urls": [ # Url to download the package. The first one must be morphux servers
                "https://install.morphux.org/packages/glibc-2.24.tar.xz"
            ]
        }
        return self.config

    def     before(self):
        res = self.e(["mkdir", "-vp", "build"])
        os.chdir("build")
        return res

    def     configure(self):
        return self.e(["../configure",
                "--prefix=/tools",
                "--host=" + self.conf_lst["target"],
                "--build=$(../scripts/config.guess)",
                "--enable-kernel=2.6.32",
                "--with-headers=/tools/include",
                "libc_cv_forced_unwind=yes",
                "libcv_cv_c_cleanup=yes"
            ], shell=True)

    def     make(self):
        return self.e(["make", "-j", self.conf_lst["cpus"]])

    def     install(self):
        return self.e(["make", "install"])
