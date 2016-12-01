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
# linux_headers_p1.py
# Created: 01/12/2016
# By: Louis Solofrizzo <louis@morphux.org>
##

import      os

class   Linux_Headers_P1:

    conf_lst = {}
    e = False
    root_dir = ""

    def     init(self, c_lst, ex, root_dir):
        self.conf_lst = c_lst
        self.e = ex
        self.root_dir = root_dir
        self.config = {
            "name": "linux-headers", # Name of the package
            "version": "4.7.2", # Version of the package
            "size": 666, # Size of the installed package (MB)
            "archive": "linux-4.7.2.tar.xz", # Archive name
            "SBU": 0.1, # SBU (Compilation time)
            "tmp_install": True, # Is this package part of the temporary install
            "next": "glibc", # Next package to install
            "configure": False,
            "make": False,
            "urls": [ # Url to download the package. The first one must be morphux servers
                "https://install.morphux.org/packages/linux-4.7.2.tar.xz"
            ]
        }
        return self.config

    def     before(self):
        return self.e(["make", "mrproper"])

    def     install(self):
        return self.e(["make", "INSTALL_HDR_PATH=dest", "headers_install"])

    def     after(self):
        # DO NOT WORK
        return self.e(["cp", "-v", "dest/include/*", "/tools/include"])
