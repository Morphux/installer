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

class Config:

    key = 0
    quit = 1
    is_input = 1
    current_string = "morphux"
    choices = ["ACCEPT", "CANCEL"]
    current_choice = 0

    def     init(self):
        self.config = {
            "id": 1,
            "title": "Config",
            "type": "inputs"
        }
        return self.config

    def     input(self, key):
        self.key = key
        if (self.is_input and self.current_choice == 0):
            if (key == curses.KEY_BACKSPACE or key == 127 or key == 0x7f):
                self.current_string = self.current_string[:-1]
            elif (key > 31 and key < 127):
                self.current_string += str(chr(key))
        if (key == 9):
            if (self.current_choice < 2):
                curses.curs_set(0)
                self.current_choice += 1
            else:
                curses.curs_set(1)
                self.current_choice = 0;

    def     center(self, win, y, x, string, attr = 0):
        win.addstr(y, (x / 2) - len(string) / 2, string, attr)

    def     input_s(self, win, y, x):
        flag = 0
        start_x = int((x * 0.25) / 2)
        if (self.current_choice == 0):
            flag |= curses.color_pair(4)
        win.addstr(y, start_x, self.current_string, curses.A_REVERSE | flag)
        j = start_x + len(self.current_string)
        while j < x - start_x:
            win.addstr(y, j, " ", curses.A_REVERSE | flag)
            j += 1
        win.move(y, start_x + len(self.current_string))

    def     show_choices(self, win, x, y):
        t_len = 0
        i = 0
        for s in self.choices:
            t_len += len(s)
        x = (x / 2) - ((t_len + 9) / 2)
        for s in self.choices:
            flag = 0
            win.addstr(y, x, "<")
            if i == 0:
                flag = curses.color_pair(3)
            else:
                flag = curses.color_pair(1)
            if (i + 1 == self.current_choice):
                flag |= curses.A_BOLD | curses.A_REVERSE
            win.addstr(y, x + 1, s, flag)
            x += 1 + len(s)
            win.addstr(y, x, ">     ")
            x += 6
            i += 1


    def     refresh(self, win):
        if (self.current_choice == 0):
            curses.curs_set(1)
        size = win.getmaxyx()
        self.center(win, 2, size[1], "SET YOUR HOSTNAME", curses.A_BOLD)
        self.show_choices(win, size[1], 6)
        if (self.is_input == 1):
            self.input_s(win, 4, size[1])
        return self.quit
