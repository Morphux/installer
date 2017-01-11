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
# dhcpd_opt.py
# Created: 11/01/2017
# By: Louis Solofrizzo <louis@morphux.org>
##

import      os

class   Dhcpd_Opt:

    conf_lst = {}
    e = False
    root_dir = ""

    def     init(self, c_lst, ex, root_dir):
        self.conf_lst = c_lst
        self.e = ex
        self.root_dir = root_dir
        self.config = {
            "name": "dhcpd", # Name of the package
            "version": "6.11.3", # Version of the package
            "size": 2.7, # Size of the installed package (MB)
            "archive": "dhcpcd-6.11.3.tar.xz", # Archive name
            "SBU": 0.1, # SBU (Compilation time)
            "optionnal": True, # Is this package part of the temporary install
            "before": False,
            "urls": [ # Url to download the package. The first one must be morphux servers
                "https://install.morphux.org/packages/dhcpcd-6.11.3.tar.xz"
            ]
        }
        return self.config

    def     configure(self):
        return self.e(["./configure",
                    "--libexecdir=/lib/dhcpd",
                    "--dbdir=/var/lib/dhcpd"
        ])

    def     make(self):
        return self.e(["make", "-j", self.conf_lst["cpus"]])

    def     install(self):
        return self.e(["make", "install"])

    def     after(self):
        return self.e(["install", "-m", "755", "sysv/services/dhcpd", "/lib/services"])
