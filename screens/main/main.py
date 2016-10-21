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
    menu_s = ["INSTALL", "INSTALL 64BITS", "OPTIONS", "HELP", "QUIT"]
    menu_choice = 0
    quit = 0
    title = "  __  __                  _                \n\
 |  \\/  |                | |               \n\
 | \\  / | ___  _ __ _ __ | |__  _   ___  __\n\
 | |\\/| |/ _ \\| '__| '_ \\| '_ \\| | | \ \\/ /\n\
 | |  | | (_) | |  | |_) | | | | |_| |>  < \n\
 |_|  |_|\\___/|_|  | .__/|_| |_|\\__,_/_/\\_\\\n\
                   | |                     \n\
                   |_|                     \n\
"

    def     init(self):
        self.config = {
            "id": 0,
            "title": "Main",
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
                self.quit = self.menu_choice

    def     print_title(self, win):
        size = win.getmaxyx()
        y = size[0] / 4;
        x = (size[1] / 2) - (44 / 2)
        for c in self.title:
            win.addstr(y, x, c, curses.color_pair(2) | curses.A_BOLD)
            x = x + 1
            if c == '\n':
                y = y + 1
                x = (size[1] / 2) - (44 / 2)
        return y

    def     menu(self, y, win):
        size = win.getmaxyx()
        i = 0
        for string in self.menu_s:
            if i == self.menu_choice:
                win.addstr(y, (size[1] / 2) - (len(string) / 2), string, curses.color_pair(1) | curses.A_BOLD)
            else:
                win.addstr(y, (size[1] / 2) - (len(string) / 2), string)
            y += 1
            i += 1

    def     print_borders(self, win, y, height):
        size = win.getmaxyx()
        c = "#"
        i = 0
        while i < height:
            win.addstr(y + i, (size[1] / 2) - (80 / 2), c)
            i += 1
        i = 0
        while i < height + 1:
            win.addstr(y + i, (size[1] / 2) + (80 / 2), c)
            i += 1
        i = 0
        while i < 80:
            win.addstr(y, (size[1] / 2) - (80 / 2) + i, c)
            i += 1
        i = 0
        y += height
        while i < 80:
            win.addstr(y, (size[1] / 2) - (80 / 2) + i, c)
            i += 1

    def     refresh(self, win):
        size = win.getmaxyx()
        y = self.print_title(win) + 1
        win.addstr(y, (size[1] / 2) - 8, "__Installer v1__", curses.A_REVERSE)
        self.print_borders(win, y + 3, len(self.menu_s) + 5)
        self.menu(y + 6, win);
        return self.quit
