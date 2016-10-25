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
# network.py
# Created: 25/10/2016
# By: Louis Solofrizzo <louis@morphux.org>
##

import curses
import os.path
import stat

class Network:

    key = 0
    quit = 3
    main = 0

    def     init(self, main):
        self.main = main
        self.config = {
            "id": 3,
            "title": "Network",
            "type": "input",
            "input": [
                {
                    "name": "ip",
                    "title": "ENTER YOUR LOCAL IP",
                    "default": "192.168.0.1",
                    "type": "text",
                    "function": self.ip
                },
                {
                    "name": "netmask",
                    "title": "NETMASK",
                    "default": "255.255.255.255",
                    "type": "text",
                    "function": self.netmask
                },
                {
                    "name": "gateway",
                    "title": "ENTER YOUR GATEWAY",
                    "default": "",
                    "type": "text",
                    "function": self.gateway
                },
                {
                    "name": "dns",
                    "title": "ENTER YOUR DNS",
                    "default": "8.8.8.8,4.4.4.4",
                    "type": "text",
                    "function": self.dns
                },
            ]
        }
        return self.config

    def     ip(self, string):
        if len(string):
            self.main.config("network.ip", string)
            return 1
        self.main.error("IP cannot be blank")
        return 0

    def     netmask(self, string):
        if len(string):
            self.main.config("network.netmask", string)
            return 1
        self.main.error("Netmask cannot be blank")
        return 0

    def     gateway(self, string):
        if len(string):
            self.main.config("network.gateway", string)
            return 1
        self.main.error("Gateway cannot be blank")
        return 0


    def     dns(self, string):
        if len(string):
            self.main.config("network.dns", string)
            return 1
        self.main.error("DNS cannot be blank")
        return 0

    def     reset(self):
        self.quit = 3

    def     refresh(self, win):
        return self.quit
