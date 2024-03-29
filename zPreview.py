#coding: utf-8

import tkinter as tk
from tkinter import ttk, messagebox
from functools import partial
from path import Path
from PIL import Image, ImageTk
from defaults import zDefault
from zLog import get_logger

logger = get_logger("zTextureReducer")

def recolor(img: Image, alpha: bool, **options):
    # Alpha channel take 1 color
    # QUANTIZE with kmeans != 0
    # FOR ALPHA IS MANDATORY 2 (3depends on a lib)
    colors_count = options["colors"]["colors"] if not alpha else options["colors"]["colors"] - 1
    result = img.quantize(
        colors=colors_count,
        method=2,
        kmeans=0)
    if options["dither"] and options["colors"]["mode"] != "LA":
        # utilizing underlying imaging core C library directly
        # maybe implementing custom algorithm would be better
        # also reorganizing the chain of operations for recoloring 
        # (by better understanding different parts at work and properly chaining them)
        dithered = img._new(img.im.convert(options["colors"]["mode"], Image.FLOYDSTEINBERG, result.im))
        dithered = dithered.quantize(colors=colors_count)
        return dithered
    result = result.convert(
        mode=options["colors"]["mode"],
        palette=Image.ADAPTIVE,
        colors=colors_count)
    return result

def resize(img: Image, **options):
    return img.resize(
        size=(options["width"],options["height"]),
        resample=options["sampling"]
        )

def zoom(img: Image, zoom):
    resize = (img.width * zoom, img.height * zoom)
    return img.resize(size=resize, resample=Image.NEAREST)

def process_image(img: Image, **options) -> Image:
    alpha = None
    size = (img.width, img.height)
    """
    if (img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info)) and options["alpha_keep"]:
        try:
            alpha = img.getchannel("A")
        except ValueError as err:
            warn_msg = "An image has an alpha information but something is off when getting it\n" \
                "---\n" \
                "Error message is : \n" \
                "{}\n".format(err)
            #messagebox.showerror("Error", warn_msg)
            #img.info.pop("transparency", None)
            print(" -- WARNING -- ")
            print(warn_msg)
            alpha = False
    elif (img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info)) and (not options["alpha_keep"]):
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        elif img.mode == 'LA':
            img = img.convert('L')
        img.info.pop("transparency", None)
        alpha = False
    if options["order"]:
        if options["recolor"]:
            img = recolor(img, alpha, **options)
        if options["resize"]:
            img = resize(img, **options)
    else:
        if options["resize"]:
            img = resize(img, **options)
        if options["recolor"]:
            img = recolor(img, alpha, **options)
    if alpha and options["alpha_keep"]:
        if options["order"]:
            if options["recolor"]:
                dithering = Image.FLOYDSTEINBERG if options["dither"] else Image.NONE
                alpha = alpha.convert(mode="1", dither=dithering)
            if options["resize"]:
                alpha = alpha.resize((options["width"], options["height"]), Image.NEAREST)
        else:
            if options["resize"]:
                alpha = alpha.resize((options["width"], options["height"]), Image.NEAREST)
            if options["recolor"]:
                dithering = Image.FLOYDSTEINBERG if options["dither"] else Image.NONE
                alpha = alpha.convert(mode="1", dither=dithering)
        img.putalpha(alpha)
    """
    try:
        tmp = img.convert(mode="RGBA")
        if options["alpha_keep"]:
            try:
                alpha = tmp.getchannel("A")
            except ValueError as err:
                warn_msg = "An image has an alpha information but something is off when getting it\n" \
                    "---\n" \
                    "Error message is : \n" \
                    "{}\n".format(err)
                #messagebox.showerror("Error", warn_msg)
                #img.info.pop("transparency", None)
                logger.warn(" -- WARNING -- ")
                logger.warn(warn_msg)
                alpha = None
        else:
            tmp = tmp.convert(mode="RGB")
        if options["order"]:
            if options["recolor"]:
                tmp = recolor(tmp, alpha != None, **options)
            if options["resize"]:
                tmp = resize(tmp, **options)
        else:
            if options["resize"]:
                tmp = resize(tmp, **options)
            if options["recolor"]:
                tmp = recolor(tmp, alpha != None, **options)
        if alpha != None and options["alpha_keep"]:
            if options["order"]:
                if options["recolor"]:
                    dithering = Image.FLOYDSTEINBERG if options["dither"] else Image.NONE
                    alpha = alpha.convert(mode="1", dither=dithering)
                if options["resize"]:
                    alpha = alpha.resize((options["width"], options["height"]), Image.NEAREST)
            else:
                if options["resize"]:
                    alpha = alpha.resize((options["width"], options["height"]), Image.NEAREST)
                if options["recolor"]:
                    dithering = Image.FLOYDSTEINBERG if options["dither"] else Image.NONE
                    alpha = alpha.convert(mode="1", dither=dithering)
            tmp.putalpha(alpha)
        img = tmp
    except Exception as e:
        err_msg = f"Processing error : {type(e)} : {e}"
        logger.warn(err_msg)
    return img

def convert_options(**options):
    real = {}
    for key in options.keys():
        if options[key] in zPreview.sampling_conv.keys():
            real[key] = zPreview.sampling_conv[options[key]]
        elif options[key] in zPreview.colors_conv.keys():
            real[key] = zPreview.colors_conv[options[key]]
        elif options[key] in zPreview.order_conv.keys():
            real[key] = zPreview.order_conv[options[key]]
        else:
            real[key] = options[key]
    return real

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
            "mode" : "LA",
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
        self.zoompreview_frame = tk.Frame(self.container)
        zoompreview_label = tk.Label(self.zoompreview_frame,
                                     text="Zoom preview :")
        zoompreview_label.pack(side="left")
        self.zoompreview_value = tk.IntVar()
        self.zoompreview_value.set(self.options["zoom"])
        self.zoompreview_options = ttk.OptionMenu(
            self.zoompreview_frame,
            self.zoompreview_value,
            self.zoompreview_value.get(),
            *zDefault.zoom,
            command=partial(self._forward_options, "zoom", self.zoompreview_value))
        self.zoompreview_options.pack(side="left")
        self.zoompreview_frame.pack(side="top")
        self.img_container = tk.Label(self.container, anchor="center")
        self.img_container.pack(expand=True)
        self.image_path = None
        self.container.pack(expand=True, fill="both")
        self.__return_preview_size = 0
        pass

    def _forward_options(self, key: str, var: tk.Variable, *unused):
        option = {}
        option[key] = var.get()
        self.set_options(**option)
        
    def _update_preview(self):
        return_preview_size = 0
        options = convert_options(**self.options)
        if self.image_path:
            tmp_pil = Image.open(self.image_path)
            if options["preview"]:
                tmp_pil = process_image(tmp_pil, **options)
                return_preview_size = len(tmp_pil.getdata())
            tmp_pil = zoom(tmp_pil, options["zoom"])
            self.image_preview = ImageTk.PhotoImage(tmp_pil)
            self.img_container.configure(image=self.image_preview)
        self.__return_preview_size = return_preview_size

    def on_image_select_update(self, img):
        img = Path(img)
        if img.exists():
            self.image_path = img.abspath()
        else:
            self.image_path = None
        self._update_preview()

    def set_options(self, *args, **kwargs):
        update = False
        updates_entry = [key for key in kwargs.keys() if key in self.options.keys()]
        for key in updates_entry:
            self.options[key] = kwargs[key]
            update = True
        if update:
            self._update_preview()

    def get_preview_size(self) -> int:
        return self.__return_preview_size

    def export_queue(self, queue_getter, export_path):
        if queue_getter:
            queue = queue_getter()
            if len(queue) == 0:
                raise Exception("Export queue empty\nNo item in queue")
            options = convert_options(**self.options)
            for item in queue:
                img_path = Path(item[0])
                res_path = export_path / item[1] + img_path.ext
                img = Image.open(img_path.abspath())
                img = process_image(img, **options)
                img.save(res_path.abspath())
            messagebox.showinfo("Done","Finish exporting queue")
