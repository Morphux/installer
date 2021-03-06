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
# gettext_p1.py
# Created: 09/12/2016
# By: Louis Solofrizzo <louis@morphux.org>
##

import      os

class   Gettext_P1:

    conf_lst = {}
    e = False
    root_dir = ""

    def     init(self, c_lst, ex, root_dir):
        self.conf_lst = c_lst
        self.e = ex
        self.root_dir = root_dir
        self.config = {
            "name": "gettext", # Name of the package
            "version": "0.19.8.1", # Version of the package
            "size": 164, # Size of the installed package (MB)
            "archive": "gettext-0.19.8.1.tar.xz", # Archive name
            "SBU": 0.9, # SBU (Compilation time)
            "tmp_install": True, # Is this package part of the temporary install
            "next": "grep", # Next package to install
            "after": False,
            "urls": [ # Url to download the package. The first one must be morphux servers
                "https://install.morphux.org/packages/gettext-0.19.8.1.tar.xz"
            ]
        }
        return self.config

    def     before(self):
        os.chdir("gettext-tools")
        return "", 0

    def     configure(self):
        return self.e(["EMACS=NO", "./configure",
                "--prefix=/tools",
                "--disable-shared"
        ], shell=True)

    def     make(self):
        self.e(["make", "-C", "gnulib-lib",  "-j", self.conf_lst["cpus"]])
        self.e(["make", "-C", "intl", "pluralx.c",  "-j", self.conf_lst["cpus"]])
        self.e(["make", "-C", "src", "msgfmt",  "-j", self.conf_lst["cpus"]])
        self.e(["make", "-C", "src", "msgmerge",  "-j", self.conf_lst["cpus"]])
        return self.e(["make", "-C", "src", "xgettext",  "-j", self.conf_lst["cpus"]])

    def     install(self):
        self.e(["cp", "-v", "src/msgfmt", "/tools/bin"])
        self.e(["cp", "-v", "src/msgmerge", "/tools/bin"])
        return self.e(["cp", "-v", "src/xgettext", "/tools/bin"])
