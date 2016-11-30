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
# binutils_p1.py
# Created: 29/11/2016
# By: Louis Solofrizzo <louis@morphux.org>
##

class   Binutils_P1:

    conf_lst = {}
    e = False

    def init(self, c_lst, ex):
        self.conf_lst = c_lst
        self.e = ex
        self.config = {
            "name": "binutils", # Name of the package
            "version": "2.27", # Version of the package
            "size": 519, # Size of the installed package (MB)
            "archive": "binutils-2.27.tar.bz2", # Archive name
            "cheksum": "2869c9bf3e60ee97c74ac2a6bf4e9d68", # Checksum of the archive
            "SBU": 1, # SBU (Compilation time)
            "tmp_install": True, # Is this package part of the temporary install
            "next": "test2", # Next package to install
            "urls": [ # Url to download the package. The first one must be morphux servers
                "https://install.morphux.org/packages/binutils-2.27.tar.bz2",
                "http://ftp.gnu.org/gnu/binutils/binutils-2.27.tar.bz2",
            ]
        }
        return self.config
