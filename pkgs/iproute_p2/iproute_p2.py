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
# iproute_p2.py
# Created: 22/12/2016
# By: Louis Solofrizzo <louis@morphux.org>
##

import      os

class   Iproute_P2:

    conf_lst = {}
    e = False
    root_dir = ""

    def     init(self, c_lst, ex, root_dir):
        self.conf_lst = c_lst
        self.e = ex
        self.root_dir = root_dir
        self.config = {
            "name": "iproute", # Name of the package
            "version": "4.7.0", # Version of the package
            "size": 11, # Size of the installed package (MB)
            "archive": "gzip-1.8.tar.xz", # Archive name
            "SBU": 0.2, # SBU (Compilation time)
            "tmp_install": False, # Is this package part of the temporary install
            "next": False, # Next package to install
            "after": False,
            "configure": False,
            "urls": [ # Url to download the package. The first one must be morphux servers
                "https://install.morphux.org/packages/gzip-1.8.tar.xz"
            ]
        }
        return self.config

    def     before(self):
        self.e(["sed", "-i", "/ARPD/d", "Makefile"])
        self.e(["sed", "-i", "s/arpd.8//", "man/man8/Makefile"])
        self.e(["rm", "-v", "doc/arpd.sgml"])
        return self.e(["sed", "-i", "s/m_ipt.o//", "Makefile"])

    def     make(self):
        return self.e(["make", "-j", self.conf_lst["cpus"]])

    def     install(self):
        return self.e(["make", "DOCDIR=/usr/share/doc/iproute2-4.7.0", "install"])
