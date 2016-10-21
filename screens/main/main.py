################################### LICENSE ####################################
# Copyright 2016 Louis Solofrizzo                                              #
#                                                                              #
# Licensed under the Apache License, Version 2.0 (the "License");              #
# you may not use this file except in compliance with the License.             #
# You may obtain a copy of the License at                                      #
#                                                                              #
#     http://www.apache.org/licenses/LICENSE-2.0                               #
#                                                                              #
# Unless required by applicable law or agreed to in writing, software          #
# distributed under the License is distributed on an "AS IS" BASIS,            #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.     #
# See the License for the specific language governing permissions and          #
# limitations under the License.                                               #
################################################################################

##
# main.py
# Created: 21/10/2016
# By: Louis Solofrizzo <louis@morphux.org>
##

import curses

class Main:

    key = 0
    menu_s = ["INSTALL", "INSTALL 64BITS", "OPTIONS", "QUIT"]
    menu_choice = 0
    quit = 0

    def     init(self):
        self.config = {
            "id": 0,
            "title": "MENU",
            "type": "menu"
        }
        return self.config

    def     input(self, key):
        self.key = key
        if (key == curses.KEY_DOWN and self.menu_choice < len(self.menu_s) - 1):
            self.menu_choice += 1
        elif (key == curses.KEY_UP and self.menu_choice > 0):
            self.menu_choice -= 1
        elif (key == curses.KEY_ENTER or key == 10 or key == 13):
            if (self.menu_s[self.menu_choice] == "QUIT"):
                self.quit = -1
            else:
                self.quit = self.menu_choice + 1

    def     menu(self, y, win, lines):
        size = win.getmaxyx()
        i = 0
        for string in self.menu_s:
            if i == self.menu_choice:
                win.addstr(y, (size[1] / 2) - (len(string) / 2), string, curses.color_pair(1) | curses.A_BOLD)
            else:
                win.addstr(y, (size[1] / 2) - (len(string) / 2), string, curses.A_BOLD)
            if (lines and string != "QUIT"):
                win.addstr(y + 1, (size[1] / 2) - (20 / 2), "--------------------")
                y += 2
            else:
                y += 1
            i += 1

    def     refresh(self, win):
        size = win.getmaxyx()
        if (size[0] > 10):
            self.menu((size[0] / 2) - (len(self.menu_s) / 2), win, 1);
        else:
            self.menu((size[0] / 2) - (len(self.menu_s) / 2), win, 0);
        return self.quit
