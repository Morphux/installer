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
# curses.py
# Created: 21/10/2016
# By: Louis Solofrizzo <louis@morphux.org>
##

# Imports

import  curses
import  os

class   Screen:

    # Variables
    stdscr = {}
    modules = {}
    screens = {}
    curr_screen = {}

    # Construct function
    def     __init__(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(1)
        curses.start_color()
        curses.curs_set(0)
        self.load_screens()
        self.init_colors()

    # Destructor function
    def     __del__(self):
        curses.nocbreak()
        self.stdscr.keypad(0)
        curses.echo()
        curses.curs_set(1)
        os.system('stty sane')
        os.system('clear')

    # Load differents modules in the path screens/
    def     load_screens(self, path = "screens"):
        res = {}
        lst = os.listdir(path)
        dir = []
        for d in lst:
            s = os.path.abspath(path) + os.sep + d
            if os.path.isdir(s) and os.path.exists(s + os.sep + "__init__.py"):
                dir.append(d)
        for d in dir:
            res[d] = __import__(path + "." + d + "." + d, fromlist = ["*"])
            res[d] = getattr(res[d], d.title())
        self.modules = res
        self.get_screens_infos()

    # Get infos on screens
    def     get_screens_infos(self):
        config = {}
        for name, klass in self.modules.items():
            print("Reading"+ name +"module...")
            klass = klass()
            config = klass.init()
            self.screens[name] = klass
            if config["title"] == "Main":
                self.curr_screen = klass
            print("Done !")

    def     init_colors(self):
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)

    # Main Loop
    def     loop(self):
        quit = 0
        key = 0
        self.curr_screen.refresh(self.stdscr)
        self.stdscr.refresh()
        while quit != -1:
            if self.curr_screen.config["type"] == "menu":
                key = self.stdscr.getch()
                self.curr_screen.input(key)
            self.stdscr.clear()
            quit = self.curr_screen.refresh(self.stdscr)
            self.stdscr.refresh()
