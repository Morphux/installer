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
# ncurses_p1.py
# Created: 08/12/2016
# By: Louis Solofrizzo <louis@morphux.org>
##

import      os

class   Ncurses_P1:

    conf_lst = {}
    e = False
    root_dir = ""

    def     init(self, c_lst, ex, root_dir):
        self.conf_lst = c_lst
        self.e = ex
        self.root_dir = root_dir
        self.config = {
            "name": "ncurses", # Name of the package
            "version": "6.0", # Version of the package
            "size": 38, # Size of the installed package (MB)
            "archive": "ncurses-6.0.tar.gz", # Archive name
            "SBU": 0.5, # SBU (Compilation time)
            "tmp_install": True, # Is this package part of the temporary install
            "next": "bash", # Next package to install
            "after": False,
            "urls": [ # Url to download the package. The first one must be morphux servers
                "https://install.morphux.org/packages/ncurses-6.0.tar.gz"
            ]
        }
        return self.config

    def     before(self):
        return self.e(["sed", "-i", "s/mawk//", "configure"])

    def     configure(self):
        return self.e(["./configure",
                "--prefix=/tools",
                "--with-shared",
                "--without-debug",
                "--without-ada",
                "--enable-widec",
                "--enable-overwrite"
            ])

    def     make(self):
        return self.e(["make", "-j", self.conf_lst["cpus"]])

    def     install(self):
        return self.e(["make", "install"])
