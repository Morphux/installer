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
# pkgconfig_p2.py
# Created: 19/12/2016
# By: Louis Solofrizzo <louis@morphux.org>
##

import      os

class   Pkgconfig_P2:

    conf_lst = {}
    e = False
    root_dir = ""

    def     init(self, c_lst, ex, root_dir):
        self.conf_lst = c_lst
        self.e = ex
        self.root_dir = root_dir
        self.config = {
            "name": "pkg-config", # Name of the package
            "version": "0.29.1", # Version of the package
            "size": 28, # Size of the installed package (MB)
            "archive": "pkg-config-0.29.1.tar.gz", # Archive name
            "SBU": 0.3, # SBU (Compilation time)
            "tmp_install": False, # Is this package part of the temporary install
            "next": "ncurses", # Next package to install
            "before": False,
            "after": False,
            "urls": [ # Url to download the package. The first one must be morphux servers
                "https://install.morphux.org/packages/pkg-config-0.29.1.tar.gz"
            ]
        }
        return self.config

    def     configure(self):
        return self.e(["./configure",
                "--prefix=/usr",
                "--with-internal-glib",
                "--disable-compile-warnings",
                "--disable-host-tool",
                "--docdir=/usr/share/doc/pkgconfig-0.29.1"
        ])

    def     make(self):
        return self.e(["make", "-j", self.conf_lst["cpus"]])

    def     install(self):
        return self.e(["make", "install"])
