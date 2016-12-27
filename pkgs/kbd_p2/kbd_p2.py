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
# kbd_p2.py
# Created: 22/12/2016
# By: Louis Solofrizzo <louis@morphux.org>
##

import      os

class   Kbd_P2:

    conf_lst = {}
    e = False
    root_dir = ""

    def     init(self, c_lst, ex, root_dir):
        self.conf_lst = c_lst
        self.e = ex
        self.root_dir = root_dir
        self.config = {
            "name": "kbd", # Name of the package
            "version": "2.0.3", # Version of the package
            "size": 29, # Size of the installed package (MB)
            "archive": "kbd-2.0.3.tar.xz", # Archive name
            "SBU": 0.1, # SBU (Compilation time)
            "tmp_install": False, # Is this package part of the temporary install
            "next": "libpipeline", # Next package to install
            "after": False,
            "urls": [ # Url to download the package. The first one must be morphux servers
                "https://install.morphux.org/packages/kbd-2.0.3.tar.xz"
            ]
        }
        return self.config

    def     before(self):
        self.e(["patch", "-Np1", "-i", "../kbd-2.0.3-backspace-1.patch"])
        self.e(["sed", "-i", "s/\(RESIZECONS_PROGS=\)yes/\1no/g", "configure"])
        return self.e(["sed", "-i", "s/resizecons.8 //", "docs/man/man8/Makefile.in"])

    def     configure(self):
        return self.e(["PKG_CONFIG_PATH=/tools/lib/pkgconfig", "./configure",
            "--prefix=/usr",
            "--disable-vlock"
        ])

    def     make(self):
        return self.e(["make", "-j", self.conf_lst["cpus"]])

    def     install(self):
        return self.e(["make", "DOCDIR=/usr/share/doc/iproute2-4.7.0", "install"])
