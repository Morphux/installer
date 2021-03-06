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
# inetutils_p2.py
# Created: 21/12/2016
# By: Louis Solofrizzo <louis@morphux.org>
##

import      os

class   Inetutils_P2:

    conf_lst = {}
    e = False
    root_dir = ""

    def     init(self, c_lst, ex, root_dir):
        self.conf_lst = c_lst
        self.e = ex
        self.root_dir = root_dir
        self.config = {
            "name": "inetutils", # Name of the package
            "version": "1.9.4", # Version of the package
            "size": 27, # Size of the installed package (MB)
            "archive": "inetutils-1.9.4.tar.xz", # Archive name
            "SBU": 0.4, # SBU (Compilation time)
            "tmp_install": False, # Is this package part of the temporary install
            "next": "perl", # Next package to install
            "after": False,
            "urls": [ # Url to download the package. The first one must be morphux servers
                "https://install.morphux.org/packages/inetutils-1.9.4.tar.xz"
            ]
        }
        return self.config

    def     before(self):
        return self.e(["patch", "-Np1", "-i", "../inetutils-1.9.4.patch"])

    def     configure(self):
        return self.e(["./configure",
                "--prefix=/usr",
                "--localstatedir=/var",
                "--disable-logger",
                "--disable-whois",
                "--disable-rcp",
                "--disable-rexec",
                "--disable-rlogin",
                "--disable-rsh",
                "--disable-servers",
            ])

    def     make(self):
        return self.e(["make", "-j", self.conf_lst["cpus"]])

    def     install(self):
        return self.e(["make", "install"])

    def     after(self):
        self.e(["mv -v /usr/bin/{hostname,ping,ping6,traceroute} /bin"], shell=True)
        return self.e(["mv", "-v", "/usr/bin/ifconfig", "/sbin"])
