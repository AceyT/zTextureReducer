#coding: utf-8

import tkinter as tk
from tkinter import ttk
from Tooltip import Tooltip
from path import Path

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
        self.queue.heading("#0", text="Files to process", anchor=tk.W)
        self.queue.pack(side="top", expand=True, fill="both")

    def _add_cb(self):
        if self.get_selected is not None:
            selection = self.get_selected()
            for item in selection:
                self.queue.insert("", "end", text=item)

    def _remove_cb(self):
        print(self.queue.selection())
        print(*self.queue.selection())
        self.queue.delete(*self.queue.selection())

    def remove_all(self):
        self.queue.delete(*self.queue.get_children())

    def get_queue(self):
        ret = []
        for item in self.queue.get_children():
            ret.append(self.queue.item(item,'text'))
        return ret