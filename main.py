#coding: utf-8

from functools import partial
import tkinter as tk

from zLog import get_logger
from zWorkspace import zWorkspace
from zQueue import zQueue
from zOptions import zOption
from zPreview import zPreview

logger = get_logger("zTextureReducer")

win = tk.Tk()
win.title("zTextureReducer")

frame_workspace = tk.Frame(win)
frame_queue = tk.Frame(win)
frame_options = tk.Frame(win)
frame_preview = tk.Frame(win)

workspace = zWorkspace(frame_workspace)
queue = zQueue(frame_queue, add_callback=workspace.get_selection_and_unselect)
preview = zPreview(frame_preview)
workspace.bind_dclick_select(preview.on_image_select_update)
options = zOption(frame_options,
                  on_options_modified=preview.set_options,
                  on_export=partial(preview.export_queue, queue.get_queue),
                  get_preview_size=preview.get_preview_size)

frame_workspace.grid(column=0, row=0, sticky="nesw")
frame_queue.grid(column=0, row=1, sticky="nesw")
frame_preview.grid(column=1, row=0, sticky="nesw")
frame_options.grid(column=1, row=1, sticky="nesw")

win.columnconfigure(0, weight=6, minsize=400)
win.columnconfigure(1, weight=4, minsize=200)
win.rowconfigure(0, weight=5)
win.rowconfigure(1, weight=5)

win.mainloop()