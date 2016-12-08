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
# expect_p1.py
# Created: 08/12/2016
# By: Louis Solofrizzo <louis@morphux.org>
##

import      os

class   Expect_P1:

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
            "size": 4.3, # Size of the installed package (MB)
            "archive": "expect5.45.tar.gz", # Archive name
            "SBU": 0.1, # SBU (Compilation time)
            "tmp_install": True, # Is this package part of the temporary install
            "next": "dejagnu", # Next package to install
            "chdir": False,
            "after": False,
            "urls": [ # Url to download the package. The first one must be morphux servers
                "https://install.morphux.org/packages/expect5.45.tar.gz"
            ]
        }
        return self.config

    def     before(self):
        os.chdir("expect5.45")
        self.e(["cp", "-v", "configure", "configure.orig"])
        return self.e(["sed", "s:/usr/local/bin:/bin:", "configure.orig", ">", "configure"], shell=True)

    def     configure(self):
        return self.e(["./configure",
                "--prefix=/tools",
                "--with-tcl=/tools/lib",
                "--with-tclinclude=/tools/include"
            ])

    def     make(self):
        return self.e(["make", "-j", self.conf_lst["cpus"]])

    def     install(self):
        return self.e(["make", "SCRIPTS=\"\"", "install"], shell=True)
