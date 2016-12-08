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
# coreutils_p1.py
# Created: 08/12/2016
# By: Louis Solofrizzo <louis@morphux.org>
##

import      os

class   Coreutils_P1:

    conf_lst = {}
    e = False
    root_dir = ""

    def     init(self, c_lst, ex, root_dir):
        self.conf_lst = c_lst
        self.e = ex
        self.root_dir = root_dir
        self.config = {
            "name": "coreutils", # Name of the package
            "version": "8.25", # Version of the package
            "size": 132, # Size of the installed package (MB)
            "archive": "coreutils-8.25.tar.xz", # Archive name
            "SBU": 0.6, # SBU (Compilation time)
            "tmp_install": True, # Is this package part of the temporary install
            "next": "diffutils", # Next package to install
            "before": False,
            "after": False,
            "urls": [ # Url to download the package. The first one must be morphux servers
                "https://install.morphux.org/packages/coreutils-8.25.tar.xz"
            ]
        }
        return self.config

    def     configure(self):
        os.environ["FORCE_UNSAFE_CONFIGURE"] = "1"
        return self.e(["./configure",
                "--prefix=/tools",
                "--enable-install-program=hostname"
        ])

    def     make(self):
        return self.e(["make", "-j", self.conf_lst["cpus"]])

    def     install(self):
        return self.e(["make", "install"])
