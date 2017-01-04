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
# perl_p2.py
# Created: 21/12/2016
# By: Louis Solofrizzo <louis@morphux.org>
##

import      os

class   Perl_P2:

    conf_lst = {}
    e = False
    root_dir = ""

    def     init(self, c_lst, ex, root_dir):
        self.conf_lst = c_lst
        self.e = ex
        self.root_dir = root_dir
        self.config = {
            "name": "perl", # Name of the package
            "version": "5.24.0", # Version of the package
            "size": 1.3, # Size of the installed package (MB)
            "archive": "perl-5.24.0.tar.bz2", # Archive name
            "SBU": 1.3, # SBU (Compilation time)
            "tmp_install": False, # Is this package part of the temporary install
            "next": "xmlparser", # Next package to install
            "after": False,
            "urls": [ # Url to download the package. The first one must be morphux servers
                "https://install.morphux.org/packages/perl-5.24.0.tar.bz2"
            ]
        }
        return self.config

    def     before(self):
        return self.e(["echo \"127.0.0.1 localhost $(hostname)\" > /etc/hosts"], shell=True)

    def     configure(self):
        os.environ["BUILD_ZLIB"] = "False"
        os.environ["BUILD_BZIP2"] = "0"
        return self.e(["sh", "Configure", "-des",
                "-Dprefix=/usr",
                "-Dvendorprefix=/usr",
                "-Dman1dir=/usr/share/man/man1",
                "-Dman3dir=/usr/share/man/man3",
                "-Dpager='/usr/bin/less -isR'",
                "-Duseshrplib"
            ])

    def     make(self):
        return self.e(["make", "-j", self.conf_lst["cpus"]])

    def     install(self):
        return self.e(["make", "install"])
