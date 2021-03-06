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
# toolchain_p2.py
# Created: 14/12/2016
# By: Louis Solofrizzo <louis@morphux.org>
##

import      os

class   Toolchain_P2:

    conf_lst = {}
    e = False
    root_dir = ""

    def     init(self, c_lst, ex, root_dir):
        self.conf_lst = c_lst
        self.e = ex
        self.root_dir = root_dir
        self.config = {
            "name": "toolchain", # Name of the package
            "version": "", # Version of the package
            "size": 0, # Size of the installed package (MB)
            "archive": "tzdata2016f.tar.gz", # Archive name
            "SBU": 0, # SBU (Compilation time)
            "tmp_install": False, # Is this package part of the temporary install
            "next": "zlib", # Next package to install
            "configure": False,
            "make": False,
            "install": False,
            "after": False,
            "chdir": False,
            "urls": [
                "https://install.morphux.org/packages/tzdata2016f.tar.gz"
            ],
        }
        return self.config

    def     before(self):
        self.e(["mv", "-v", "/tools/bin/ld", "/tools/bin/ld-old"])
        self.e(["mv -v /tools/$(uname -m)-pc-linux-gnu/bin/{ld,ld-old}"], shell=True, ignore=True)
        self.e(["mv", "-v", "/tools/bin/{ld-new,ld}"], shell=True)
        self.e(["gcc -dumpspecs | sed -e 's@/tools@@g' -e '/\*startfile_prefix_spec:/{n;s@.*@/usr/lib/ @}' -e '/\*cpp:/{n;s@$@ -isystem /usr/include@}' > `dirname $(gcc --print-libgcc-file-name)`/specs"], shell=True)
        return self.e(["ln", "-sv", "/tools/bin/ld", "/tools/$(uname -m)-pc-linux-gnu/bin/ld"], shell=True)
