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
# gcc_p2.py
# Created: 16/12/2016
# By: Louis Solofrizzo <louis@morphux.org>
##

import      os

class   Gcc_P2:

    conf_lst = {}
    e = False
    root_dir = ""

    def     init(self, c_lst, ex, root_dir):
        self.conf_lst = c_lst
        self.e = ex
        self.root_dir = root_dir
        self.config = {
            "name": "gcc", # Name of the package
            "version": "6.2.0", # Version of the package
            "size": 3300, # Size of the installed package (MB)
            "archive": "gcc-6.2.0.tar.bz2", # Archive name
            "SBU": 79, # SBU (Compilation time)
            "tmp_install": False, # Is this package part of the temporary install
            "next": "bzip2", # Next package to install
            "urls": [ # Url to download the package. The first one must be morphux servers
                "https://install.morphux.org/packages/gcc-6.2.0.tar.bz2"
            ]
        }
        return self.config

    def     before(self):
        self.e(["mkdir", "-pv", "build"])
        os.chdir("build")
        return "", 0

    def     configure(self):
        return self.e(["SED=sed ../configure",
                    "--prefix=/usr",
                    "--enable-languages=c,c++",
                    "--disable-multilib",
                    "--disable-bootstrap",
                    "--with-system-zlib"
                ], shell=True)

    def     make(self):
        return self.e(["make", "-j", self.conf_lst["cpus"]])

    def     install(self):
        return self.e(["make", "install"])

    def     after(self):
        self.e(["ln", "-sv", "../usr/bin/cpp", "/lib"])
        self.e(["ln", "-sv", "gcc", "/usr/bin/cc"])
        self.e(["install", "-v", "-dm755", "/usr/lib/bfd-plugins"])
        self.e(["ln", "-sfv", 
            "../../libexec/gcc/$(gcc -dumpmachine)/6.2.0/liblto_plugin.so",
            "/usr/lib/bfd-plugins/"], shell=True)
        self.e(["mkdir", "-pv", "/usr/share/gdb/auto-load/usr/lib/"])
        self.e(["mv", "-v", "/usr/lib/*gdb.py", "/usr/share/gdb/auto-load/usr/lib"], shell=True)
