#coding: utf-8

"""zEntryPopup.py
Base code by  dakov   15Sep2013

https://stackoverflow.com/questions/18562123/how-to-make-ttk-treeviews-rows-editable

"""

import tkinter as tk
from tkinter import ttk

class zEntryPopup(ttk.Entry):

    def __init__(self, parent, text, validation_cb, **kw):
        ''' If relwidth is set, then width is ignored '''
        super().__init__(parent, **kw)

        self.insert(0, text) 
        #self['state'] = 'readonly'
        self['background'] = 'white'
        #self['selectbackground'] = '#1BA1E2'
        self['exportselection'] = False
        self.on_validate = validation_cb
        self.focus_force()
        self.bind("<Control-a>", self.selectAll)
        self.bind("<Escape>", lambda *ignore: self.destroy())
        self.bind("<Return>", self.validate)
        self.bind('<FocusOut>', lambda *ignore: self.destroy())

    def selectAll(self, *ignore):
        ''' Set selection on the whole text '''
        self.selection_range(0, 'end')
        # returns 'break' to interrupt default key-bindings
        return 'break'

    def validate(self, *ignore):
        if self.on_validate is not None:
            self.on_validate(self.get())
        self.destroy()