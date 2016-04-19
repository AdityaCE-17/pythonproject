# -*- coding: utf-8 -*-
"""
Created on Wed Apr 06 20:17:45 2016

@author: vhd
"""

from Tkinter import *

import hangman

root = Tk()
root.title ("Mega Microgames Collection")

mainframe = Frame(root, height = 200, width = 500)
mainframe.pack_propagate(0)
mainframe.pack(padx = 5, pady = 5)

intro = Label(mainframe, text = """Mega Microgames Collection.
Please select one of the following games to play:
""")
intro.pack(side = TOP)

hm_button = Button(mainframe, text = "Hangman", command = hangman.gui)
hm_button.pack()

exit_button = Button(mainframe, text = "Quit", command = root.destroy)
exit_button.pack(side = BOTTOM)

root.mainloop()