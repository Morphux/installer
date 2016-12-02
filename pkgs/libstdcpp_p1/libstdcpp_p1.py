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
# libstdcpp_p1.py
# Created: 02/12/2016
# By: Louis Solofrizzo <louis@morphux.org>
##

import      os

class   Libstdcpp_P1:

    conf_lst = {}
    e = False
    root_dir = ""

    def     init(self, c_lst, ex, root_dir):
        self.conf_lst = c_lst
        self.e = ex
        self.root_dir = root_dir
        self.config = {
            "name": "libstdcpp", # Name of the package
            "version": "6.2.0", # Version of the package
            "size": 666, # Size of the installed package (MB)
            "archive": "gcc-6.2.0.tar.bz2", # Archive name
            "SBU": 0.4, # SBU (Compilation time)
            "tmp_install": True, # Is this package part of the temporary install
            "after": False,
            "next": False, # Next package to install
            "chdir": False,
            "urls": [ # Url to download the package. The first one must be morphux servers
                "https://install.morphux.org/packages/gcc-6.2.0.tar.bz2"
            ]
        }
        return self.config

    def     before(self):
        os.chdir("gcc-6.2.0")
        res = self.e(["rm", "-rf", "build"])
        res = self.e(["mkdir", "-vp", "build"])
        os.chdir("build")
        return res

    def     configure(self):
        return self.e(["../configure",
                "--prefix=/tools",
                "--host=" + self.conf_lst["target"],
                "--disable-multilib",
                "--disable-nls",
                "--disable-libstdcxx-threads",
                "--disable-libstdcxx-pch",
                "--with-gxx-include-dir=/tools/"+ self.conf_lst["target"] +"/include/c++/6.2.0"
            ])

    def     make(self):
        return self.e(["make", "-j", self.conf_lst["cpus"]])

    def     install(self):
        return self.e(["make", "install"])
