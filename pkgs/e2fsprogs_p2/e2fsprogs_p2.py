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
# e2fsprogs_p2.py
# Created: 21/12/2016
# By: Louis Solofrizzo <louis@morphux.org>
##

import      os

class   E2Fsprogs_P2:

    conf_lst = {}
    e = False
    root_dir = ""

    def     init(self, c_lst, ex, root_dir):
        self.conf_lst = c_lst
        self.e = ex
        self.root_dir = root_dir
        self.config = {
            "name": "e2fsprogs", # Name of the package
            "version": "1.43.1", # Version of the package
            "size": 54, # Size of the installed package (MB)
            "archive": "", # Archive name
            "SBU": 2.1, # SBU (Compilation time)
            "tmp_install": False, # Is this package part of the temporary install
            "next": "coreutils", # Next package to install
            "after": False,
            "urls": [ # Url to download the package. The first one must be morphux servers
                "https://install.morphux.org/packages/"
            ]
        }
        return self.config

    def     before(self):
        self.e(["sed -i -e 's:\[\.-\]::' tests/filter.sed"], shell=True)
        res = self.e(["mkdir", "build"])
        os.chdir("build")
        return res

    def     configure(self):
        os.environ["LIBS"] = "-L/tools/lib"
        os.environ["CFLAGS"] = "-I/tools/include"
        os.environ["PKG_CONFIG_PATH"] = "/tools/lib/pkgconfig"
        return self.e(["./configure",
                "--prefix=/usr",
                "--bindir=/bin",
                "--with-root-prefix=''",
                "--enable-elf-shlibs",
                "--disable-libblkid",
                "--disable-libuuid",
                "--disable-uuidd",
                "--disable-fsck"
        ], shell=True)

    def     make(self):
        return self.e(["make", "-j", self.conf_lst["cpus"]])

    def     install(self):
        self.e(["make", "install"])
        self.e(["make", "install-libs"])
        self.e(["chmod -v u+w /usr/lib/{libcom_err,libe2p,libext2fs,libss}.a"], shell=True)
        self.e(["gunzip -v /usr/share/info/libext2fs.info.gz"], shell=True)
        self.e(["install-info --dir-file=/usr/share/info/dir /usr/share/info/libext2fs.info"], shell=True)
        self.e(["makeinfo -o doc/com_err.info ../lib/et/com_err.texinfo"], shell=True)
        self.e(["install -v -m644 doc/com_err.info /usr/share/info"], shell=True)
        return self.e(["install-info --dir-file=/usr/share/info/dir /usr/share/info/com_err.info"], shell=True)
