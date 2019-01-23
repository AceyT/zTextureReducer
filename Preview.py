#coding: utf-8

import tkinter as tk
from tkinter import ttk
from path import Path
from PIL import Image, ImageTk
from defaults import zDefault

def recolor(img: Image, **options):
    return img.convert(
        mode=options["colors"]["mode"],
        palette=Image.ADAPTIVE,
        dither=options["dither"],
        colors=options["colors"]["colors"] )

def resize(img: Image, **options):
    return img.resize(
        size=(options["width"],options["height"]),
        resample=options["sampling"]
        )

class zPreview:

    sampling_conv = {
        "Nearest":Image.NEAREST,
        "Box":Image.BOX,
        "Bilinear":Image.BILINEAR,
        "Hamming":Image.HAMMING,
        "Bicubic":Image.BICUBIC,
        "Lanczos":Image.LANCZOS
    }

    colors_conv = {
        "Greyscale" : {
            "mode" : "L",
            "colors" : 256
        },
        "16 Colors Palette" : {
            "mode" : "P",
            "colors" : 16
        },
        "256 Colors Palette"  : {
            "mode" : "P",
            "colors" : 256
        }
    }
    order_conv = {
        "Resize first" : 0,
        "Recolor first" : 1
    }

    def __init__(self, master: tk.BaseWidget, **kwargs):
        self.container = ttk.LabelFrame(master, text="Preview",
                                        width=150, height=150)
        self.options = zDefault.config.copy()
        self.img_container = tk.Label(self.container, anchor="center")
        self.img_container.pack(expand=True)
        self.image_path = None
        self.container.pack(expand=True, fill="both")
        pass

    def set_options(self, *args, **kwargs):
        update = False
        updates_entry = [key for key in kwargs.keys() if key in self.options.keys()]
        for key in updates_entry:
            self.options[key] = kwargs[key]
            update = True
        if update:
            self._update_preview()

    def on_image_select_update(self, img):
        img = Path(img)
        if img.exists():
            self.image_path = img.abspath()
        else:
            self.image_path = None
        self._update_preview()

    def _convert_options(self):
        real = {}
        for key in self.options.keys():
            if self.options[key] in zPreview.sampling_conv.keys():
                real[key] = zPreview.sampling_conv[self.options[key]]
            elif self.options[key] in zPreview.colors_conv.keys():
                real[key] = zPreview.colors_conv[self.options[key]]
            elif self.options[key] in zPreview.order_conv.keys():
                real[key] = zPreview.order_conv[self.options[key]]
            else:
                real[key] = self.options[key]
        return real
        
    def _update_preview(self):
        options = self._convert_options()
        if self.image_path:
            tmp_pil = Image.open(self.image_path)
            if options["preview"]:
                if options["order"]:
                    if options["recolor"]:
                        tmp_pil = recolor(tmp_pil, **options)
                    if options["resize"]:
                        tmp_pil = resize(tmp_pil, **options)
                else:
                    if options["resize"]:
                        tmp_pil = resize(tmp_pil, **options)
                    if options["recolor"]:
                        tmp_pil = recolor(tmp_pil, **options)
            self.image_preview = ImageTk.PhotoImage(tmp_pil)
            self.img_container.configure(image=self.image_preview)
