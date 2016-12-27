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
# vim_p2.py
# Created: 24/12/2016
# By: Louis Solofrizzo <louis@morphux.org>
##

import      os

class   Vim_P2:

    conf_lst = {}
    e = False
    root_dir = ""

    def     init(self, c_lst, ex, root_dir):
        self.conf_lst = c_lst
        self.e = ex
        self.root_dir = root_dir
        self.config = {
            "name": "vim", # Name of the package
            "version": "7.4", # Version of the package
            "size": 109, # Size of the installed package (MB)
            "archive": "vim-7.4.tar.bz2", # Archive name
            "SBU": 1, # SBU (Compilation time)
            "tmp_install": False, # Is this package part of the temporary install
            "next": False, # Next package to install
            "urls": [ # Url to download the package. The first one must be morphux servers
                "https://install.morphux.org/packages/vim-7.4.tar.bz2"
            ]
        }
        return self.config

    def     before(self):
        return self.e(["echo '#define SYS_VIMRC_FILE \"/etc/vimrc\"' >> src/feature.h"], shell=True)

    def     configure(self):
        return self.e(["./configure",
                "--prefix=/usr",
        ])

    def     make(self):
        return self.e(["make", "-j", self.conf_lst["cpus"]])

    def     install(self):
        return self.e(["make", "install"])

    def     after(self):
        self.e(["ln", "-sv", "vim", "/usr/bin/vi"])
        return self.e(["ln", "-sv", "../vim/vim74/doc", "/usr/share/doc/vim-7.4"])
