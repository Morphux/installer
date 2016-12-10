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
# perl_p1.py
# Created: 09/12/2016
# By: Louis Solofrizzo <louis@morphux.org>
##

import      os

class   Perl_P1:

    conf_lst = {}
    e = False
    root_dir = ""

    def     init(self, c_lst, ex, root_dir):
        self.conf_lst = c_lst
        self.e = ex
        self.root_dir = root_dir
        self.config = {
            "name": "perl", # Name of the package
            "version": "5.2.4", # Version of the package
            "size": 1.3, # Size of the installed package (MB)
            "archive": "perl-5.24.0.tar.bz2", # Archive name
            "SBU": 1.3, # SBU (Compilation time)
            "tmp_install": True, # Is this package part of the temporary install
            "next": "sed", # Next package to install
            "before": False,
            "after": False,
            "urls": [ # Url to download the package. The first one must be morphux servers
                "https://install.morphux.org/packages/perl-5.24.0.tar.bz2"
            ]
        }
        return self.config

    def     configure(self):
        return self.e(["sh", "Configure",
                "-des",
                "-Dprefix=/tools",
                "-Dlibs=-lm"
            ])

    def     make(self):
        return self.e(["make", "-j", self.conf_lst["cpus"]])

    def     install(self):
        self.e(["cp", "-v", "perl", "cpan/podlators/scripts/pod2man", "/tools/bin"])
        self.e(["mkdir", "-pv", "/tools/lib/perl5/5.24.0"])
        return self.e(["cp", "-Rv", "lib/*", "/tools/lib/perl5/5.24.0"], shell=True)
