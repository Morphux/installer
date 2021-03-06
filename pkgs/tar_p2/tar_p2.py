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
# tar_p2.py
# Created: 24/12/2016
# By: Louis Solofrizzo <louis@morphux.org>
##

import      os

class   Tar_P2:

    conf_lst = {}
    e = False
    root_dir = ""

    def     init(self, c_lst, ex, root_dir):
        self.conf_lst = c_lst
        self.e = ex
        self.root_dir = root_dir
        self.config = {
            "name": "tar", # Name of the package
            "version": "1.29", # Version of the package
            "size": 40, # Size of the installed package (MB)
            "archive": "tar-1.29.tar.xz", # Archive name
            "SBU": 2.2, # SBU (Compilation time)
            "tmp_install": False, # Is this package part of the temporary install
            "next": "texinfo", # Next package to install
            "before": False,
            "after": False,
            "urls": [ # Url to download the package. The first one must be morphux servers
                "https://install.morphux.org/packages/tar-1.29.tar.xz"
            ]
        }
        return self.config

    def     configure(self):
        os.environ["FORCE_UNSAFE_CONFIGURE"] = "1"
        return self.e(["./configure",
                "--prefix=/usr",
                "--bindir=/bin"
        ])

    def     make(self):
        return self.e(["make", "-j", self.conf_lst["cpus"]])

    def     install(self):
        return self.e(["make", "install"])
