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
# mandb_p2.py
# Created: 23/12/2016
# By: Louis Solofrizzo <louis@morphux.org>
##

import      os

class   Mandb_P2:

    conf_lst = {}
    e = False
    root_dir = ""

    def     init(self, c_lst, ex, root_dir):
        self.conf_lst = c_lst
        self.e = ex
        self.root_dir = root_dir
        self.config = {
            "name": "man-db", # Name of the package
            "version": "2.7.5", # Version of the package
            "size": 30, # Size of the installed package (MB)
            "archive": "", # Archive name
            "SBU": 0.4, # SBU (Compilation time)
            "tmp_install": False, # Is this package part of the temporary install
            "next": False, # Next package to install
            "before": False,
            "urls": [ # Url to download the package. The first one must be morphux servers
                "https://install.morphux.org/packages/"
            ]
        }
        return self.config

    def     configure(self):
        return self.e(["./configure",
            "--prefix=/usr",
            "--docdir=/usr/share/doc/man-db-2.7.5",
            "--sysconfdir=/etc",
            "--disable-setuid",
            "--with-browser=/usr/bin/lynx",
            "--with-vgrind=/usr/bin/vgrind",
            "--with-grap=/usr/bin/grap"
        ])

    def     make(self):
        return self.e(["make", "-j", self.conf_lst["cpus"]])

    def     install(self):
        return self.e(["make", "install"])

    def     after(self):
        return self.e(["sed", "-i", "s:man root:root root:g", "/usr/lib/tmpfiles.d/man-db.conf"])
