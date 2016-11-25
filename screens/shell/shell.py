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
# shell.py
# Created: 16/11/2016
# By: Louis Solofrizzo <louis@morphux.org>
##

# These imports are here for the Popen function, used in main()
from subprocess import call
from subprocess import Popen, PIPE

class   Shell:

##
# Variables
##

    dlg = 0  # Dialog object
    conf_lst = {} # List object for configuration

##
# Functions
##

    # Init function, called by Main instance
    def     init(self, dialog, config_list):
        self.dlg = dialog
        self.conf_lst = config_list
        self.config = {
            "id": 4,
            "name": "Shell"
        }
        return self.config

    # main function, called by Main instance
    def     main(self, Main):
        # Execute the binary /bin/sh
        # Note there is no error handling, nor output redirection.
        sh = Popen(['/bin/sh'])
        sh.wait()
        return 0
