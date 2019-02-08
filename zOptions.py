#coding: utf-8

import tkinter as tk
from tkinter import ttk, messagebox
from Tooltip import Tooltip
from path import Path
from functools import partial
from defaults import zDefault

def set_state(frame_widget: tk.Frame, value:int):
    _state = "normal" if value else "disabled"
    for child in frame_widget.winfo_children():
        try:
            child.configure(state=_state)
        except:
            if type(child) == tk.Frame:
                set_state(child, value)

class zOption:

    def __init__(self, master: tk.BaseWidget, **kwargs):
        self.container = ttk.LabelFrame(
            master,
            text="Options",
            width=200,
            height=100)
        self.container.pack(side="top", expand=True, fill="both", anchor="e")
        self.option_callback = kwargs.get("on_options_modified", None)
        self.export_callback = kwargs.get("on_export", None)
        config = zDefault.config.copy()
        # Options controls
        self.optionframe = tk.Frame(self.container)
        self.preview_value = tk.IntVar(self.optionframe)
        self.preview_value.set(config["preview"])
        self.preview_toggle = ttk.Checkbutton(
            self.optionframe, 
            text="Preview modifications",
            variable=self.preview_value,
            command=partial(self._update_fromvar, "preview", self.preview_value))
        self.preview_toggle.pack(side="top", expand=False, anchor="w")
        sep1 = ttk.Separator(self.optionframe)
        sep1.pack(side="top", expand=True, fill="x")
        # # Resize Controls
        self.resize_value = tk.IntVar()
        self.resize_value.set(config["resize"])
        self.resize_toggle = ttk.Checkbutton(self.optionframe,
                                             text="Resize",
                                             variable=self.resize_value,
                                             command=self._toggle_resize)
        self.resize_toggle.pack(side="top", expand=False, anchor="w")
        # # # Sizing
        self.resizeframe = tk.Frame(self.optionframe)
        width = ttk.Label(self.resizeframe, text="Width :")
        width.pack(side="left")
        self.width_value = tk.IntVar()
        self.width_value.set(config["width"])
        self.width_select = ttk.OptionMenu(
            self.resizeframe,
            self.width_value,
            self.width_value.get(), 
            *zDefault.sizes,
            command=partial(self._update_fromvar, "width", self.width_value))
        self.width_select.pack(side="left")
        height = ttk.Label(self.resizeframe, text="Height :")
        height.pack(side="left")
        self.height_value = tk.IntVar()
        self.height_value.set(config["height"])
        self.height_select = ttk.OptionMenu(
            self.resizeframe,
            self.height_value,
            self.height_value.get(),
            *zDefault.sizes,
            command=partial(self._update_fromvar, "height", self.height_value))
        self.height_select.pack(side="left")
        self.resizeframe.pack(side="top", anchor="w")
        # # # Sampling
        self.samplingframe = tk.Frame(self.optionframe)
        self.sampling_value = tk.StringVar()
        self.sampling_value.set(config["sampling"])
        sampling = ttk.Label(self.samplingframe, text="Sampling mode :")
        sampling.pack(side="left")
        self.sampling_select = ttk.OptionMenu(
            self.samplingframe,
            self.sampling_value,
            self.sampling_value.get(),
            *zDefault.sampling_modes,
            command=partial(self._update_fromvar, "sampling", self.sampling_value))
        self.sampling_select.pack(side="left")
        self.samplingframe.pack(side="top", anchor="w")
        sep2 = ttk.Separator(self.optionframe)
        sep2.pack(side="top", expand=True, fill="x")
        # # Recolor controls
        self.recolor_value = tk.IntVar()
        self.recolor_value.set(config["recolor"])
        self.recolor_toggle = ttk.Checkbutton(self.optionframe,
                                              text="Modify Color Mode",
                                              variable=self.recolor_value,
                                              command=self._toggle_recolor)
        self.recolor_toggle.pack(side="top", expand=False, anchor="w")
        self.recolorframe = tk.Frame(self.optionframe)
        # # # Color mode
        self.colormodeframe = tk.Frame(self.recolorframe)
        self.colormode_value = tk.StringVar()
        self.colormode_value.set(config["colors"])
        colormode = ttk.Label(self.colormodeframe, text="Color mode :")
        colormode.pack(side="left")
        self.colormode_select = ttk.OptionMenu(
            self.colormodeframe,
            self.colormode_value,
            self.colormode_value.get(),
            *zDefault.color_modes,
            command=partial(self._update_fromvar, "colors", self.colormode_value))
        self.colormode_select.pack(side="left", expand=False)
        self.colormodeframe.pack(side="top", anchor="w")
        # # # Dither
        self.ditherframe = tk.Frame(self.recolorframe)
        self.dither_value = tk.IntVar()
        self.dither_value.set(config["dither"])
        self.dither_toggle = ttk.Checkbutton(
            self.ditherframe,
            text="Dithering",
            variable=self.dither_value,
            command=partial(self._update_fromvar, "dither", self.dither_value))
        self.dither_toggle.pack(side="left")
        self.ditherframe.pack(side="top", anchor="w")
        # # # Alpha
        self.alphaframe = tk.Frame(self.recolorframe)
        self.alpha_value = tk.IntVar()
        self.alpha_value.set(config["alpha_keep"])
        self.alpha_toggle = ttk.Checkbutton(
            self.alphaframe,
            text="Keep alpha channel",
            variable=self.alpha_value,
            command=partial(self._update_fromvar, "alpha_keep", self.alpha_value))
        self.alpha_toggle.pack(side="left")
        self.alphaframe.pack(side="top", anchor="w")
        self.recolorframe.pack(side="top", anchor="w")
        sep3 = ttk.Separator(self.optionframe)
        sep3.pack(side="top", expand=True, fill="x")
        # # Extra
        # # # Operation Order
        order = ttk.Label(self.optionframe, text="Operation Order")
        order.pack(side="top", anchor="w")
        self.order_value = tk.StringVar()
        self.order_value.set(config["order"])
        self.order_select = ttk.OptionMenu(
            self.optionframe, 
            self.order_value,
            self.order_value.get(),
            *zDefault.order_modes,
            command=partial(self._update_fromvar, "order", self.order_value))
        self.order_select.pack(side="top", anchor="w")
        sep4 = ttk.Separator(self.optionframe)
        sep4.pack(side="top", expand=True, fill="x")
        # # # Export Location
        export = ttk.Label(self.optionframe, text="Export Location")
        export.pack(side="top", anchor="w")
        self.dirpickerframe = tk.Frame(self.optionframe)
        self.dir_entry = ttk.Entry(self.dirpickerframe)
        self.dir_entry.pack(side="left", expand=True, fill= "x")
        self.dir_button = ttk.Button(
            self.dirpickerframe,
            text="...",
            width="5",
            command=self._pick_dir)
        self.dirbutton_tooltip = Tooltip(
            self.dir_button,
            "Choose a directory where to save the resulting processed images")
        self.dir_button.pack(side="left", expand=False)
        self.dirpickerframe.pack(side="top", anchor="w", expand=True, fill="x")
        sep5 = ttk.Separator(self.optionframe)
        sep5.pack(side="top", expand=True, fill="x")
        # Export
        self.export_frame = tk.Frame(self.container)
        self.export_button = tk.Button(self.export_frame,
                                       text="EXPORT",
                                       bg="#ffdf82",
                                       activebackground="#c4ab64",
                                       relief=tk.GROOVE,
                                       border=3,
                                       command=self._on_export)
        self.export_button.pack(side="top", expand=True, fill="x")
        
        self.container.rowconfigure(0, weight=10)
        self.container.columnconfigure(0, weight=1)
        self.optionframe.grid(row=0, column=0, sticky="new")
        self.export_frame.grid(row=1, column=0, sticky="sew")
        pass

    def _toggle_resize(self):
        set_state(self.resizeframe, self.resize_value.get())
        set_state(self.samplingframe, self.resize_value.get())
        self._update_config(resize=self.resize_value.get())
        pass

    def _toggle_recolor(self):
        set_state(self.recolorframe, self.recolor_value.get())
        self._update_config(recolor=self.recolor_value.get())
        pass

    def set_option_callback(self, callback):
        self.option_callback = callback

    def set_export_callback(self, export_callback):
        self.export_callback = export_callback

    def _pick_dir(self):
        directory = tk.filedialog.askdirectory(
            initialdir="./", 
            title="Choose a directory for where to export")
        dirpath = Path(directory)
        if dirpath.exists():
            self.dir_entry.delete(0, 'end')
            self.dir_entry.insert('', dirpath.abspath())

    def _update_fromvar(self, key: str, var: tk.Variable, *unused):

        # OptionMenu gives us the changes as positional argument,
        # but Checkbutton doesn't
        # This function streamline the process of getting the value, 
        # and thus *args is here to catch some additional unused parameters

        conf = {}
        conf[key] = var.get()
        self._update_config(**conf)

    def _update_config(self, **kwargs):
        if self.option_callback:
            self.option_callback(**kwargs)

    def _on_export(self):
        try:
            export_path = Path(self.dir_entry.get())
            if export_path.exists() and self.export_callback:
                self.export_callback(export_path)
            elif not export_path.exists():
                err = "Invalid export path : doesn't exists\n" \
                "Given path : [{}]".format(export_path.abspath())
                raise Exception(err)
        except Exception as err:
            err_msg = "Something went wrong\n" \
                "Look at the console and report the issue if there is anything\n\n" \
                "--- Message caught ---\n" \
                "{}".format(err)
            messagebox.showerror("Error", err_msg)
            return



