################################### LICENSE ####################################
#                      Copyright 2016 Louis Solofrizzo                         #
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
# config.py
# Created: 21/10/2016
# By: Louis Solofrizzo <louis@morphux.org>
##

import curses

class Config:

    key = 0
    quit = 1
    root_p = ""
    main = 0

    def     init(self, main):
        self.main = main
        self.config = {
            "id": 1,
            "title": "Config",
            "type": "input",
            "input": [
                {
                    "name": "hostname",
                    "title": "SET YOUR HOSTNAME",
                    "default": "morphux",
                    "type": "text",
                    "function": self.hostname
                },
                {
                    "name": "root1",
                    "title": "ROOT PASSWORD",
                    "default": "",
                    "type": "password",
                    "function": self.root_p1
                },
                {
                    "name": "root2",
                    "title": "CONFIRM ROOT PASSWORD",
                    "default": "",
                    "type": "password",
                    "function": self.root_p2
                }

            ]
        }
        return self.config

    def     input(self, key):
        self.key = key

    def     hostname(self, string):
        if len(string) == 0:
            self.main.error("Hostname cannot be empty.");
            return 0
        return 1

    def     root_p1(self, string):
        if len(string) == 0:
            self.main.error("Password cannot be empty.");
            return 0
        self.root_p = string
        return 1
    
    def     root_p2(self, string):
        if string != self.root_p:
            self.main.error("Passwords did not match !");
            return -1
        self.quit = 0
        return 1

    def     reset(self):
        self.quit = 1

    def     refresh(self, win):
        return self.quit
