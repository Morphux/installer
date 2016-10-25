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
# curses.py
# Created: 21/10/2016
# By: Louis Solofrizzo <louis@morphux.org>
##

# Imports

import  curses
import  os
from input import Input

class   Screen:

    # Variables
    stdscr = {}
    modules = {}
    screens = []
    prev_id = 0
    curr_screen = {}
    title = "  __  __                  _                \n\
 |  \\/  |                | |               \n\
 | \\  / | ___  _ __ _ __ | |__  _   ___  __\n\
 | |\\/| |/ _ \\| '__| '_ \\| '_ \\| | | \ \\/ /\n\
 | |  | | (_) | |  | |_) | | | | |_| |>  < \n\
 |_|  |_|\\___/|_|  | .__/|_| |_|\\__,_/_/\\_\\\n\
                   | |                     \n\
                   |_|                     \n\
"


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
            print("Reading "+ name +" module...")
            klass = klass()
            config = klass.init()
            self.screens.append(klass)
            if config["id"] == 0:
                self.curr_screen = klass
            print("Done !")

    # Colors init
    def     init_colors(self):
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_WHITE)

    # Print morphux title and installer version
    def     print_title(self, win):
        size = win.getmaxyx()
        y = size[0] / 7;
        x = (size[1] / 2) - (44 / 2)
        for c in self.title:
            win.addstr(y, x, c, curses.color_pair(2) | curses.A_BOLD)
            x = x + 1
            if c == '\n':
                y = y + 1
                x = (size[1] / 2) - (44 / 2)
        win.addstr(y + 1, (size[1] / 2) - 8, "__Installer v1__", curses.A_REVERSE)
        return y

    def     change_screen(self, id):
        for s in self.screens:
            if s.config["id"] == id:
                self.prev_id = self.curr_screen.config["id"]
                self.curr_screen = s
                s.reset()

    # Main Loop
    def     loop(self):
        quit = 0
        key = 0
        c_input = 0
        input = Input()
        size = self.stdscr.getmaxyx()
        height =  size[0] / 4
        if height < 10:
            height = 10
        win = curses.newwin(height, int(size[1] * 0.75), self.print_title(self.stdscr) + 2, int(size[1] * 0.25 / 2))
        win.border()
        self.curr_screen.refresh(win)
        self.stdscr.leaveok(1)
        self.stdscr.refresh()
        win.refresh()
        while quit != -1:
            key = self.stdscr.getch()
            if self.curr_screen.config["type"] == "menu":
                self.curr_screen.input(key)
            elif self.curr_screen.config["type"] == "input":
                c_input += input.input(key)
                if c_input >= len(self.curr_screen.config["input"]):
                    c_input = -1
                elif c_input < 0:
                    self.change_screen(self.prev_id)
                    c_input = 0
            win.erase()
            if self.curr_screen.config["type"] == "input" and c_input >= 0:
                conf = self.curr_screen.config["input"][c_input]
                input.s_input(win, conf["title"], conf["default"], conf["function"], conf["type"])
            quit = self.curr_screen.refresh(win)
            if (quit != self.curr_screen.config["id"]):
                win.erase()
                self.change_screen(quit)
                if self.curr_screen.config["type"] == "input":
                    conf = self.curr_screen.config["input"][c_input]
                    input.s_input(win, conf["title"], conf["default"], conf["function"], conf["type"])
                else:
                    c_input = 0
                self.curr_screen.refresh(win)
            win.border()
            self.stdscr.refresh()
            win.refresh()
