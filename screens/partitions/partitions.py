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
# partitions.py
# Created: 25/10/2016
# By: Louis Solofrizzo <louis@morphux.org>
##

import curses
import os.path
import stat

class Partitions:

    key = 0
    quit = 2
    main = 0

    def     init(self, main):
        self.main = main
        self.config = {
            "id": 2,
            "title": "Partitions",
            "type": "input",
            "input": [
                {
                    "name": "disk",
                    "title": "ENTER DISK NAME",
                    "default": "/dev/sda",
                    "type": "text",
                    "function": self.disk
                },
               {
                    "name": "grub",
                    "title": "ENTER GRUB PARTITION",
                    "default": "1",
                    "type": "text",
                    "function": self.grub
                },
               {
                    "name": "root",
                    "title": "ENTER ROOT PARTITION",
                    "default": "2",
                    "type": "text",
                    "function": self.root
                },
               {
                    "name": "swap",
                    "title": "ENTER SWAP PARTITION",
                    "default": "3",
                    "type": "text",
                    "function": self.swap
                },
               {
                    "name": "boot",
                    "title": "ENTER BOOT PARTITION",
                    "default": "4",
                    "type": "text",
                    "function": self.boot
                },
               {
                    "name": "home",
                    "title": "ENTER HOME PARTITION",
                    "default": "5",
                    "type": "text",
                    "function": self.home
                },
            ]
        }
        return self.config

    def     exist(self, string):
        try:
            return stat.S_ISBLK(os.stat(string).st_mode)
        except:
            return False

    def     disk(self, string):
        if self.exist(string):
            self.main.config("partitions.disk", string)
            self.config["input"][1]["default"] = string + self.config["input"][1]["default"]
            self.config["input"][2]["default"] = string + self.config["input"][2]["default"]
            self.config["input"][3]["default"] = string + self.config["input"][3]["default"]
            self.config["input"][4]["default"] = string + self.config["input"][4]["default"]
            self.config["input"][5]["default"] = string + self.config["input"][5]["default"]
            return 1
        self.main.error("Disk " + string + " cannot be found")
        return 0

    def     grub(self, string):
        if self.exist(string):
            self.main.config("partitions.grub", string)
            return 1
        self.main.error("Partition " + string + " cannot be found")
        return 0

    def     root(self, string):
        if self.exist(string):
            self.main.config("partitions.root", string)
            return 1
        self.main.error("Partition " + string + " cannot be found")
        return 0

    def     swap(self, string):
        if self.exist(string):
            self.main.config("partitions.swap", string)
            return 1
        self.main.error("Partition " + string + " cannot be found")
        return 0

    def     boot(self, string):
        if self.exist(string):
            self.main.config("partitions.boot", string)
            return 1
        self.main.error("Partition " + string + " cannot be found")
        return 0

    def     home(self, string):
        if self.exist(string):
            self.quit = 3
            self.main.config("partitions.home", string)
            return 1
        self.main.error("Partition " + string + " cannot be found")
        return 0

    def     reset(self):
        self.quit = 2

    def     refresh(self, win):
        return self.quit
