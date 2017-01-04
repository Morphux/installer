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
# xz_p2.py
# Created: 21/12/2016
# By: Louis Solofrizzo <louis@morphux.org>
##

import      os

class   Xz_P2:

    conf_lst = {}
    e = False
    root_dir = ""

    def     init(self, c_lst, ex, root_dir):
        self.conf_lst = c_lst
        self.e = ex
        self.root_dir = root_dir
        self.config = {
            "name": "xz", # Name of the package
            "version": "5.2.2", # Version of the package
            "size": 15, # Size of the installed package (MB)
            "archive": "xz-5.2.2.tar.xz", # Archive name
            "SBU": 0.2, # SBU (Compilation time)
            "tmp_install": False, # Is this package part of the temporary install
            "next": "kmod", # Next package to install
            "after": False,
            "urls": [ # Url to download the package. The first one must be morphux servers
                "https://install.morphux.org/packages/xz-5.2.2.tar.xz"
            ]
        }
        return self.config

    def     before(self):
        return self.e(["sed -e '/mf\.buffer = NULL/a next->coder->mf.size = 0;' -i src/liblzma/lz/lz_encoder.c"], shell=True)

    def     configure(self):
        return self.e(["./configure",
                "--prefix=/usr",
                "--disable-static",
                "--docdir=/usr/share/doc/xz-5.2.2"
        ])

    def     make(self):
        return self.e(["make", "-j", self.conf_lst["cpus"]])

    def     install(self):
        self.e(["make", "install"])
        if "MERGE_USR" in self.conf_lst["config"] and self.conf_lst["config"]["MERGE_USR"] != True:
            self.e(["mv -v /usr/bin/{lzma,unlzma,lzcat,xz,unxz,xzcat} /bin"], shell=True)
        self.e(["mv -v /usr/lib/liblzma.so.* /lib"], shell=True)
        return self.e(["ln -svf ../../lib/$(readlink /usr/lib/liblzma.so) /usr/lib/liblzma.so"], shell=True)
