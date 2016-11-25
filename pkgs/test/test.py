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
# test.py
# Created: 25/11/2016
# By: Louis Solofrizzo <louis@morphux.org>
##

# This a temporary file, here in order to test the install process.

class   Test:

    conf_lst = {}

    def init(self, c_lst):
        self.conf_lst = c_lst
        self.config = {
            "name": "test", # Name of the package
            "version": "1.0", # Version of the package
            "size": 100, # Size of the installed package
            "archive": "test-1.0.tar.gz", # Archive name
            "cheksum": "", # Checksum of the archive
            "SBU": 1, # SBU (Compilation time)
            "tmp_install": False, # Is this package part of the temporary install
            "next": "test2", # Next package to install
            "urls": [ # Url to download the package. The first one must be morphux servers
                "http://url1.com/",
                "http://url2.com/",
            ]
        }
        return self.config
