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
# tcl_p2.py
# Created: 12/01/2017
# By: Louis Solofrizzo <louis@morphux.org>
##

import      os

class   Tcl_P2:

    conf_lst = {}
    e = False
    root_dir = ""
    sourcedir = ""

    def     init(self, c_lst, ex, root_dir):
        self.conf_lst = c_lst
        self.e = ex
        self.root_dir = root_dir
        self.config = {
            "name": "tcl", # Name of the package
            "version": "8.6.6", # Version of the package
            "size": 9.1, # Size of the installed package (MB)
            "archive": "tcl8.6.6-src.tar.gz", # Archive name
            "SBU": 1, # SBU (Compilation time)
            "tmp_install": False, # Is this package part of the temporary install
            "next": "expect", # Next package to install
            "chdir": False,
            "before": False,
            "urls": [ # Url to download the package. The first one must be morphux servers
                "https://install.morphux.org/packages/tcl8.6.6-src.tar.gz"
            ]
        }
        return self.config

    def     configure(self):
        os.chdir("tcl8.6.6")
        self.sourcedir = os.getcwd()
        os.chdir("unix")
        if (self.conf_lst["arch"] == "x86_64"):
            arg = "--enable-64bit"
        else:
            arg = ""
        return self.e(["./configure",
                "--prefix=/usr",
                "--mandir=/usr/share/man",
                arg
            ])

    def     make(self):
        return self.e(["make", "-j", self.conf_lst["cpus"]])

    def     install(self):
        s = self.sourcedir
        self.e(['sed', '-e', 's#'+ s +'/unix#/usr/lib#', '-e', 's#'+ s +'#/usr/include#', '-i', 'tclConfig.sh'])
        self.e(['sed', '-e', 's#'+ s +'/unix/pkgs/tdbc1.0.4#/usr/lib/tdbc1.0.4#', '-e', 's#'+ s +'/pkgs/tdbc1.0.4/generic#/usr/include#', '-e', 's#'+ s +'/pkgs/tdbc1.0.4/library#/usr/lib/tcl8.6#', '-e', 's#'+ s +'/pkgs/tdbc1.0.4#/usr/include#', '-i', 'pkgs/tdbc1.0.4/tdbcConfig.sh'])
        self.e(['sed', '-e', 's#'+ s +'/unix/pkgs/itcl4.0.5#/usr/lib/itcl4.0.5#', '-e', 's#'+ s +'/pkgs/itcl4.0.5/generic#/usr/include#', '-e', 's#'+ s +'/pkgs/itcl4.0.5#/usr/include#', '-i', 'pkgs/itcl4.0.5/itclConfig.sh'])
        self.e(["make", "install"])
        return self.e(["make", "install-private-headers"])

    def     after(self):
        self.e(["ln", "-vsf", "tclsh8.6", "/usr/bin/tclsh"])
        return self.e(["chmod", "-v", "755", "/usr/lib/libtcl8.6.so"])
