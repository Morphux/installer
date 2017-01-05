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
# eudev_p2.py
# Created: 22/12/2016
# By: Louis Solofrizzo <louis@morphux.org>
##

import      os

class   Eudev_P2:

    conf_lst = {}
    e = False
    root_dir = ""

    def     init(self, c_lst, ex, root_dir):
        self.conf_lst = c_lst
        self.e = ex
        self.root_dir = root_dir
        self.config = {
            "name": "eudev", # Name of the package
            "version": "3.2", # Version of the package
            "size": 77, # Size of the installed package (MB)
            "archive": "eudev-3.2.tar.gz", # Archive name
            "SBU": 0.4, # SBU (Compilation time)
            "tmp_install": False, # Is this package part of the temporary install
            "next": "util-linux", # Next package to install
            "urls": [ # Url to download the package. The first one must be morphux servers
                "https://install.morphux.org/packages/eudev-3.2.tar.gz"
            ]
        }
        return self.config

    def     before(self):
        return self.e(["sed", "-r", "-i", "s|/usr(/bin/test)|\1|", "test/udev-test.pl"])

    def     configure(self):
        return self.e(["./configure",
            "--prefix=/usr",
            "--bindir=/sbin",
            "--sbindir=/sbin",
            "--libdir=/usr/lib",
            "--sysconfdir=/etc",
            "--libexecdir=/lib",
            "--with-rootprefix=",
            "--with-rootlibdir=/lib",
            "--enable-manpages",
            "--disable-static",
            "--config-cache"
        ])

    def     make(self):
        return self.e(["LIBRARY_PATH=/tools/lib", "make", "-j", self.conf_lst["cpus"]], shell=True)

    def     install(self):
        return self.e(["make", "LD_LIBRARY_PATH=/tools/lib", "install"])

    def     after(self):
        self.e(["tar", "-xvf", "../udev-lfs-20140408.tar.bz2"])
        self.e(["make", "-f", "udev-lfs-20140408/Makefile.lfs", "install"])
        return self.e(["LD_LIBRARY_PATH=/tools/lib", "udevadm", "hwdb", "--update"])
