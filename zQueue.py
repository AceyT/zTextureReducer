#coding: utf-8

from functools import partial
import tkinter as tk
from tkinter import ttk
from Tooltip import Tooltip
from path import Path
from zEntryPopup import zEntryPopup

class zQueue:

    def __init__(self, master: tk.BaseWidget, **kwargs):
        self.container = ttk.LabelFrame(
            master,
            text="Queue", 
            width=500,
            height=100)
        self.container.pack(side="top", expand=True, fill="both")
        # Selection callback
        self.get_selected = kwargs.get("add_callback", None)
        # Controls
        self.controls = tk.Frame(self.container)
        self.add_button = ttk.Button(
            self.controls, 
            text="Add",
            command=self._add_cb)
        self.add_tooltip = Tooltip(
            self.add_button,
            "Add selected images from workspace to the queue")
        self.add_button.pack(side="left")
        self.remove_button = ttk.Button(
            self.controls,
            text="Remove",
            command=self._remove_cb)
        self.remove_tooltip = Tooltip(
            self.remove_button,
            "Remove selected images from the queue")
        self.remove_button.pack(side="left")
        self.remove_all_button = ttk.Button(
            self.controls,
            text="Remove All",
            command=self.remove_all)
        self.remove_all_button.pack(side="left")
        self.controls.pack(side="top", expand=False, anchor="w")
        # Treeview
        self.queue = ttk.Treeview(self.container, selectmode="extended")
        self.queue["columns"] = ("1")
        self.queue.heading("#0", text="Files to process", anchor=tk.W)
        self.queue.heading("1", text="Rename to", anchor=tk.W)
        self.queue["displaycolumns"] = ["1"]
        self.queue.bind("<Double-1>", self._on_dclick_item)
        self.queue.pack(side="top", expand=True, fill="both")

    def _add_cb(self):
        if self.get_selected is not None:
            selection = self.get_selected()
            for item in selection:
                fp = Path(item)
                self.queue.insert(
                    "", 
                    "end",
                    text=item,
                    values=("{}".format(fp.namebase))
                    )

    def _remove_cb(self):
        print(self.queue.selection())
        print(*self.queue.selection())
        self.queue.delete(*self.queue.selection())

    def _on_dclick_item(self, *args, **kwargs):
        """
            Method bind to double click
                used to rename a file
        """
        event = args[0]
        item = self.queue.identify_row(event.y)
        if self.queue.identify_column(event.x) == "#1" and item is not '':
            px, py, width, height = self.queue.bbox(item, "#1")
            pady = height // 2
            values = self.queue.item(item, "values")
            value = values[0] if values is not '' else ''
            self.popUp = zEntryPopup(
                self.queue,
                value,
                partial(self.set_rename, item))
            self.popUp.place(x=px, y=py+pady, anchor=tk.W, relwidth=1)

    def set_rename(self, item, name_value, *ignore):
        self.queue.item(item, values=(name_value))

    def remove_all(self):
        self.queue.delete(*self.queue.get_children())

    def get_queue(self):
        ret = []
        for item in self.queue.get_children():
            ## TODO
            ## Rework algo to properly handle renaming option
            src = self.queue.item(item, 'text')
            name = ''
            values = self.queue.item(item, 'values')
            if values is not '':
                name = values[0]
            else:
                name = Path(src).namebase
            ret.append((src, name))
        return ret

