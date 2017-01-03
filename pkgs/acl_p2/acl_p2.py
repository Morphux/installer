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
# acl_p2.py
# Created: 21/12/2016
# By: Louis Solofrizzo <louis@morphux.org>
##

import      os

class   Acl_P2:

    conf_lst = {}
    e = False
    root_dir = ""

    def     init(self, c_lst, ex, root_dir):
        self.conf_lst = c_lst
        self.e = ex
        self.root_dir = root_dir
        self.config = {
            "name": "acl", # Name of the package
            "version": "2.2.52", # Version of the package
            "size": 4.8, # Size of the installed package (MB)
            "archive": "acl-2.2.52.src.tar.gz", # Archive name
            "SBU": 0.1, # SBU (Compilation time)
            "tmp_install": False, # Is this package part of the temporary install
            "next": "libcap", # Next package to install
            "urls": [ # Url to download the package. The first one must be morphux servers
                "https://install.morphux.org/packages/acl-2.2.52.src.tar.gz"
            ]
        }
        return self.config

    def     before(self):
        self.e(["sed", "-i", "-e", "s|/@pkg_name@|&-@pkg_version@|", "include/builddefs.in"])
        self.e(["sed -i 's:| sed.*::g' test/{sbits-restore,cp,misc}.test"], shell=True)
        return self.e(["sed -i -e '/TABS-1;/a if (x > (TABS-1)) x = (TABS-1);' libacl/__acl_to_any_text.c"], shell=True)

    def     configure(self):
        return self.e(["./configure",
                "--prefix=/usr",
                "--bindir=/bin",
                "--disable-static",
                "--libexecdir=/usr/lib"
            ])

    def     make(self):
        return self.e(["make", "-j", self.conf_lst["cpus"]])

    def     install(self):
        self.e(["make", "install", "install-dev", "install-lib"])
        return self.e(["chmod", "-v", "755", "/usr/lib/libacl.so"])

    def     after(self):
        self.e(["mv -v /usr/lib/libacl.so.* /lib"], shell=True)
        return self.e(["ln -sfv ../../lib/$(readlink /usr/lib/libacl.so) /usr/lib/libacl.so"], shell=True)

