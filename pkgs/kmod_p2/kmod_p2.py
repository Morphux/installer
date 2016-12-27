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
# kmod_p2.py
# Created: 21/12/2016
# By: Louis Solofrizzo <louis@morphux.org>
##

import      os

class   Kmod_P2:

    conf_lst = {}
    e = False
    root_dir = ""

    def     init(self, c_lst, ex, root_dir):
        self.conf_lst = c_lst
        self.e = ex
        self.root_dir = root_dir
        self.config = {
            "name": "kmod", # Name of the package
            "version": "23", # Version of the package
            "size": 10.3, # Size of the installed package (MB)
            "archive": "kmod-23.tar.xz", # Archive name
            "SBU": 0.1, # SBU (Compilation time)
            "tmp_install": False, # Is this package part of the temporary install
            "next": "gettext", # Next package to install
            "after": False,
            "before": False,
            "urls": [ # Url to download the package. The first one must be morphux servers
                "https://install.morphux.org/packages/kmod-23.tar.xz"
            ]
        }
        return self.config

    def     configure(self):
        return self.e(["./configure",
                "--prefix=/usr",
                "--bindir=/bin",
                "--sysconfdir=/etc",
                "--with-rootlibdir=/lib",
                "--with-xz",
                "--with-zlib"
        ])

    def     make(self):
        return self.e(["make", "-j", self.conf_lst["cpus"]])

    def     install(self):
        self.e(["make", "install"])
        self.e(["for target in depmod insmod lsmod modinfo modprobe rmmod; do \
        ln -sfv ../bin/kmod /sbin/$target\
        done"], shell=True)
        return self.e(["ln", "-sfv", "kmod", "/bin/lsmod"])
