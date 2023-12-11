#coding: utf-8

import tkinter as tk
from tkinter import ttk, filedialog
from path import Path
from PIL import Image
from zLog import get_logger

logger = get_logger("zTextureReducer")

class zWorkspace:

    def __init__(self, master: tk.BaseWidget):
        self.container = ttk.LabelFrame(
            master,
            text="Workspace",
            width=500,
            height=100)
        self.container.pack(side="top", expand=True, fill="both")
        self.selection_callback = None
        # Controls
        self.controls = tk.Frame(self.container)
        self.add_button = ttk.Button(
            self.controls,
            text="Add Files",
            command=self._add_cb)
        self.add_button.pack(side="left")
        self.add_dir_button = ttk.Button(
            self.controls,
            text="Add Directory",
            command=self._add_dir_cb)
        self.add_dir_button.pack(side="left")
        self.remove_button = ttk.Button(
            self.controls,
            text="Remove",
            command=self._remove_cb)
        self.remove_button.pack(side="left")
        self.remove_all_button = ttk.Button(
            self.controls,
            text="Remove All",
            command=self._clean_cb)
        self.remove_all_button.pack(side="left")
        self.bonus_button = ttk.Button(self.controls, text="( ͡° ͜ʖ ͡°)")
        self.bonus_button.pack(side="left")
        self.controls.pack(side="top", expand=False, anchor="w")
        # Treeview
        self.files = ttk.Treeview(self.container, selectmode="extended")
        self.files["columns"] = ("1", "2")
        self.files.heading("#0", text="Filename", anchor=tk.W)
        self.files.heading("1", text="Size", anchor=tk.W)
        self.files.heading("2", text="Path", anchor=tk.W)
        self.files["displaycolumns"] = ["1"]
        self.files.pack(side="top", expand=True, fill="both")
        self.files.bind("<Double-1>", self._on_dclick_change)

    # Callbacks
    def _add_cb(self):
        files = tk.filedialog.askopenfilenames(
            initialdir="./",
            title="Select File(s)",
            filetypes=(("png files", "*.png"), ("bmp files", "*.bmp"), ("All Files", "*")))
        for filepath in files:
            self.add_file(Path(filepath))
        ###/*, ("jpeg files", "*.jpg"),*/ 
        ### Maybe later

    def _add_dir_cb(self):
        directory = tk.filedialog.askdirectory(
            initialdir="./",
            title="Add all images from a directory")
        dirpath = Path(directory)
        if dirpath.exists():
            for file in dirpath.files():
                self.add_file(file)


    def _remove_cb(self):
        self.files.delete(*self.files.selection())

    def _clean_cb(self):
        self.files.delete(*self.files.get_children())

    # Utility

    def add_file(self, file: Path):
        try:
            if file.exists() and file.ext in [".png", ".bmp"]:
                tmp = Image.open(file.abspath())
                tmp.load()
                size = tmp.size
                logger.debug(f"{file} ; size {size} ; mode {tmp.mode}")
                tmp.close()
                self.files.insert(
                    "",
                    "end",
                    text=file.basename(),
                    values=("{}x{}".format(*size), "{}".format(file.abspath())))
        except Exception as e:
            err_msg = f"Couldn't load <{file.abspath()}>, {type(e)} : {e}"
            logger.warn(err_msg)

    def bind_dclick_select(self, callback):
        self.selection_callback = callback
    
    def _on_dclick_change(self, *args, **kwargs):
        if self.selection_callback is not None:
            items = self.files.selection()
            if len(items):
                self.selection_callback(self.files.item(items[0], "values")[1])

    def get_selection_and_unselect(self):
        items = self.files.selection()
        ret = [ self.files.item(item, "values")[1] for item in items ]
        self.files.selection_set(*())
        return ret
