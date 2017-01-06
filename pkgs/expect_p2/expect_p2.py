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
# expect_p2.py
# Created: 06/01/2017
# By: Louis Solofrizzo <louis@morphux.org>
##

import      os

class   Expect_P2:

    conf_lst = {}
    e = False
    root_dir = ""

    def     init(self, c_lst, ex, root_dir):
        self.conf_lst = c_lst
        self.e = ex
        self.root_dir = root_dir
        self.config = {
            "name": "expect", # Name of the package
            "version": "5.45", # Version of the package
            "size": 4.1, # Size of the installed package (MB)
            "archive": "expect5.45.tar.gz", # Archive name
            "SBU": 0.2, # SBU (Compilation time)
            "tmp_install": False, # Is this package part of the temporary install
            "next": False, # Next package to install
            "chdir": False,
            "before": False,
            "urls": [ # Url to download the package. The first one must be morphux servers
                "https://install.morphux.org/packages/expect5.45.tar.gz"
            ]
        }
        return self.config

    def     configure(self):
        return self.e(["./configure",
                "--prefix=/usr",
                "--with-tcl=/usr/lib",
                "--enable-shared",
                "--mandir=/usr/share/man",
                "--with-tclinclude=/usr/include"
            ])

    def     make(self):
        return self.e(["make", "-j", self.conf_lst["cpus"]])

    def     install(self):
        return self.e(["make", "install"], shell=True)

    def     after(self):
        return self.e(["ln", "-svf", "expect5.45/libexpect5.45.so", "/usr/lib"])
