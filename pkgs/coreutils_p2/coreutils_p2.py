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
# coreutils_p2.py
# Created: 21/12/2016
# By: Louis Solofrizzo <louis@morphux.org>
##

import      os

class   Coreutils_P2:

    conf_lst = {}
    e = False
    root_dir = ""

    def     init(self, c_lst, ex, root_dir):
        self.conf_lst = c_lst
        self.e = ex
        self.root_dir = root_dir
        self.config = {
            "name": "coreutils", # Name of the package
            "version": "8.25", # Version of the package
            "size": 168, # Size of the installed package (MB)
            "archive": "coreutils-8.25.tar.xz", # Archive name
            "SBU": 2.6, # SBU (Compilation time)
            "tmp_install": False, # Is this package part of the temporary install
            "next": "diffutils", # Next package to install
            "after": False,
            "urls": [ # Url to download the package. The first one must be morphux servers
                "https://install.morphux.org/packages/coreutils-8.25.tar.xz"
            ]
        }
        return self.config

    def     before(self):
        self.e(["patch", "-Np1", "-i", "../coreutils-8.25-i18n-2.patch"])

    def     configure(self):
        os.environ["FORCE_UNSAFE_CONFIGURE"] = "1"
        return self.e(["./configure",
                "--prefix=/usr",
                "--enable-no-install-program=kill,uptime"
        ])

    def     make(self):
        return self.e(["make", "-j", self.conf_lst["cpus"]])

    def     install(self):
        self.e(["make", "install"])
        self.e(["mv -v /usr/bin/{cat,chgrp,chmod,chown,cp,date,dd,df,echo} /bin"], shell=True)
        self.e(["mv -v /usr/bin/{false,ln,ls,mkdir,mknod,mv,pwd,rm} /bin"], shell=True)
        self.e(["mv -v /usr/bin/{rmdir,stty,sync,true,uname} /bin"], shell=True)
        self.e(["mv -v /usr/bin/chroot /usr/sbin"], shell=True)
        self.e(["mv -v /usr/share/man/man1/chroot.1 /usr/share/man/man8/chroot.8"], shell=True)
        self.e(["sed -i s/\"1\"/\"8\"/1 /usr/share/man/man8/chroot.8"], shell=True)
        self.e(["mv -v /usr/bin/{head,sleep,nice,test,[} /bin"], shell=True)
