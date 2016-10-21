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
    is_input = 0
    current_string = ""

    def     init(self):
        self.config = {
            "id": 1,
            "title": "Config",
            "type": "inputs"
        }
        return self.config

    def     input(self, key):
        self.key = key
        if (key == curses.KEY_BACKSPACE or key == 127 or key == 0x7f):
            self.current_string = self.current_string[:-1]
        elif (key > 31 and key < 127):
            self.current_string += str(chr(key))

    def     center(self, win, y, x, string, attr = 0):
        win.addstr(y, (x / 2) - len(string) / 2, string, attr)

    def     input_s(self, win, y, x, default):
        if self.is_input == 0:
            self.current_string = default
            self.is_input = 1
            curses.curs_set(1)
        start_x = int((x * 0.25) / 2)
        win.addstr(y, start_x, self.current_string, curses.A_REVERSE)
        j = start_x + len(self.current_string)
        while j < x - start_x:
            win.addstr(y, j, " ", curses.A_REVERSE)
            j += 1
        win.move(y, start_x + len(self.current_string))


    def     refresh(self, win):
        size = win.getmaxyx()
        self.center(win, 2, size[1], "SET YOUR HOSTNAME", curses.A_BOLD)
        self.input_s(win, 4, size[1], "morphux")
        return self.quit
