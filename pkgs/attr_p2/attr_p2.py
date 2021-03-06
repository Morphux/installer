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
# attr_p2.py
# Created: 19/12/2016
# By: Louis Solofrizzo <louis@morphux.org>
##

import      os

class   Attr_P2:

    conf_lst = {}
    e = False
    root_dir = ""

    def     init(self, c_lst, ex, root_dir):
        self.conf_lst = c_lst
        self.e = ex
        self.root_dir = root_dir
        self.config = {
            "name": "attr", # Name of the package
            "version": "2.4.47", # Version of the package
            "size": 3.3, # Size of the installed package (MB)
            "archive": "attr-2.4.47.src.tar.gz", # Archive name
            "SBU": 0.1, # SBU (Compilation time)
            "tmp_install": False, # Is this package part of the temporary install
            "next": "acl", # Next package to install
            "urls": [ # Url to download the package. The first one must be morphux servers
                "https://install.morphux.org/packages/attr-2.4.47.src.tar.gz"
            ]
        }
        return self.config

    def     before(self):
        self.e(["sed", "-i", "-e", "s|/@pkg_name@|&-@pkg_version@|", "include/builddefs.in"])
        return self.e(["sed", "-i", "-e", '/SUBDIRS/s|man[25]||g', "man/Makefile"])

    def     configure(self):
        return self.e(["./configure",
                "--prefix=/usr",
                "--bindir=/bin",
                "--disable-static"
            ])

    def     make(self):
        return self.e(["make", "-j", self.conf_lst["cpus"]])

    def     install(self):
        self.e(["make", "install", "install-dev", "install-lib"])
        return self.e(["chmod", "-v", "755", "/usr/lib/libattr.so"])

    def     after(self):
        self.e(["mv -v /usr/lib/libattr.so.* /lib"], shell=True)
        return self.e(["ln -sfv ../../lib/$(readlink /usr/lib/libattr.so) /usr/lib/libattr.so"], shell=True)

