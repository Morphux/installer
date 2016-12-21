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
# readline_p2.py
# Created: 21/12/2016
# By: Louis Solofrizzo <louis@morphux.org>
##

import      os

class   Readline_P2:

    conf_lst = {}
    e = False
    root_dir = ""

    def     init(self, c_lst, ex, root_dir):
        self.conf_lst = c_lst
        self.e = ex
        self.root_dir = root_dir
        self.config = {
            "name": "readline", # Name of the package
            "version": "6.3", # Version of the package
            "size": 14, # Size of the installed package (MB)
            "archive": "", # Archive name
            "SBU": 0.1, # SBU (Compilation time)
            "tmp_install": False, # Is this package part of the temporary install
            "next": False, # Next package to install
            "urls": [ # Url to download the package. The first one must be morphux servers
                "https://install.morphux.org/packages/"
            ]
        }
        return self.config

    def     before(self):
        self.e(["patch", "-Np1", "-i", "../readline-6.3-upstream_fixes-3.patch"])
        self.e(["sed -i '/MV.*old/d' Makefile.in"], shell=True)
        return self.e(["sed -i '/{OLDSUFF}/c:' support/shlib-install"], shell=True)

    def     configure(self):
        return self.e(["./configure",
                "--prefix=/usr",
                "--disable-static",
                "--docdir=/usr/share/doc/readline-6.3"
        ])

    def     make(self):
        return self.e(["make", "SHLIB_LIBS=-lncurses", "-j", self.conf_lst["cpus"]])

    def     install(self):
        return self.e(["make", "SHLIB_LIBS=-lncurses", "install"])

    def     after(self):
        self.e(["mv -v /usr/lib/lib{readline,history}.so.* /lib"], shell=True)
        self.e(["ln -sfv ../../lib/$(readlink /usr/lib/libreadline.so) /usr/lib/libreadline.so"], shell=True)
        return self.e(["ln -sfv ../../lib/$(readlink /usr/lib/libhistory.so ) /usr/lib/libhistory.so"], shell=True)
