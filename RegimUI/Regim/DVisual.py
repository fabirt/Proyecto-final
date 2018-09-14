#  -*- coding: utf-8 -*-
from tkinter import Frame
from typing import Union

import cv2
import numpy
from PIL import Image, ImageEnhance, ImageTk

try:
    from Tkinter import *
except ImportError:
    from tkinter import *

# path = "C:/Users/Fabian/Desktop/Fabi_py_Projects/projects/Data_analysis/Data/Input/K/input_1.png"
# original_image = cv2.imread(path, 0)
# original_height, original_width = original_image.shape[:2]
# factor = 3
# new_width = int(original_width * factor)
# new_height = int(original_height * factor)
# resized_image = cv2.resize(original_image, (new_width, new_height))
# a = Image.fromarray(resized_image).show()


class DVisual:
    def __init__(self, top=None):
        from PIL import Image, ImageEnhance, ImageTk
        _side_bg_color = '#535353'
        _main_bg_color = '#282828'
        _fg_color = '#000000'

        _font9 = "-family Verdana -size 9 -weight normal -slant roman" \
                " -underline 0 -overstrike 0"
        _font11 = "-family Verdana -size 11 -weight normal -slant roman" \
                 " -underline 0 -overstrike 0"
        _font13 = "-family Verdana -size 13 -weight normal -slant roman " \
                 "-underline 0 -overstrike 0"

        # Creating all the GUI
        screen_width = int(top.winfo_screenwidth() * 0.85)
        screen_height = int(top.winfo_screenheight() - 76)
        padx = int((top.winfo_screenwidth() / 2) - (screen_width / 2))
        screen_size = "{0}x{1}+{2}+0".format(screen_width, screen_height, padx)
        top.geometry(screen_size)
        top.title("DVisual")
        # top.iconbitmap(self.icon_path)
        top.resizable(False, False)
        top.configure(background="#d9d9d9")

        # Frames configuration
        self.frame_images = Frame(top)
        self.frame_images.place(relx=0.0, rely=0.0, height=screen_height, width=screen_width*0.2)
        self.frame_images.configure(relief=SUNKEN)
        self.frame_images.configure(borderwidth="1")
        self.frame_images.configure(background=_side_bg_color)

        self.frame_visual = Frame(top)
        self.frame_visual.place(relx=0.2, rely=0.0, height=screen_height, width=screen_width * 0.65)
        self.frame_visual.configure(relief=SUNKEN)
        self.frame_visual.configure(borderwidth="1")
        self.frame_visual.configure(background=_main_bg_color)

        self.frame_sliders = Frame(top)
        self.frame_sliders.place(relx=0.85, rely=0.0, height=screen_height, width=screen_width * 0.15)
        self.frame_sliders.configure(relief=SUNKEN)
        self.frame_sliders.configure(borderwidth="1")
        self.frame_sliders.configure(background=_side_bg_color)

        # Thumbnail frames configuration
        Tk.update(top)
        self.tn_width = int(self.frame_images.winfo_width()) * 0.6

        self.image_frame_list = [0, 1, 2, 3]
        self.image_canvas_list = [None, None, None, None]
        for i in self.image_frame_list:
            rel_x = 0.19
            rel_y = 0.04 + (0.24 * i)
            self.image_frame_list[i] = Frame(self.frame_images)
            self.image_frame_list[i].place(relx=rel_x, rely=rel_y, height=self.tn_width, width=self.tn_width)
            self.image_frame_list[i].configure(relief=SOLID)
            self.image_frame_list[i].configure(borderwidth="1")
            self.image_frame_list[i].configure(background=_main_bg_color)
            self.image_frame_list[i].configure(cursor="hand2")

            path = Image.open("C:/Users/Fabian/Desktop/Fabi_py_Projects/projects/Data_analysis/Data/Input/K/input_1.png")
            photo = ImageTk.PhotoImage(path)
            self.image_canvas_list[i] = Canvas(self.image_frame_list[i], highlightthickness=0)
            self.image_canvas_list[i].configure(borderwidth="0")
            self.image_canvas_list[i].configure(background="#fff")
            self.image_canvas_list[i].grid(row=0, column=0, sticky='nswe')
            self.image_canvas_list[i].bind("<Button-1>", self.select_image)
            self.image_canvas_list[i].update()  # wait till canvas is created
            self.image_canvas_list[i].create_image(0, 0, anchor=NW, image=photo)
            self.image_canvas_list[i].image = photo

        # Main visualizer frame configuration
        Tk.update(top)
        visual_width = int(self.frame_visual.winfo_width())
        visual_height = int(self.frame_visual.winfo_height())
        if visual_width < visual_height:
            self.visual_size = visual_width
        else:
            self.visual_size = visual_height
        padx_visual = int((visual_width-self.visual_size) / 2)
        self.frame_visual_inner = Frame(self.frame_visual)
        self.frame_visual_inner.place(x=padx_visual, rely=0.0, height=self.visual_size, width=self.visual_size)
        self.frame_visual_inner.configure(relief=SUNKEN)
        self.frame_visual_inner.configure(borderwidth="0")
        self.frame_visual_inner.configure(background="#000")
        self.frame_visual_inner.configure(cursor="fleur")

        # Sliders configuration
        # Brightness slider
        self.scale_br = Scale(self.frame_sliders, from_=0, to=4, orient=HORIZONTAL, resolution=0.2)
        self.scale_br.place(relx=0.0, rely=0.05, relwidth=1)
        self.scale_br.configure(background=_side_bg_color)
        self.scale_br.configure(activebackground="#202020")
        self.scale_br.configure(foreground="#fff")
        self.scale_br.configure(borderwidth="0")
        self.scale_br.configure(command="")
        self.scale_br.set(1)
        # Contrast slider
        self.scale_ct = Scale(self.frame_sliders, from_=0, to=4, orient=HORIZONTAL, resolution=0.2)
        self.scale_ct.place(relx=0.0, rely=0.15, relwidth=1)
        self.scale_ct.configure(background=_side_bg_color)
        self.scale_ct.configure(activebackground="#202020")
        self.scale_ct.configure(foreground="#fff")
        self.scale_ct.configure(borderwidth="0")
        self.scale_ct.configure(command="")
        self.scale_ct.set(1)

    def select_image(self, event):
        for item in self.image_canvas_list:
            if item == event.widget:
                item.configure(borderwidth="1")
            else:
                item.configure(borderwidth="0")


if __name__ == '__main__':
    root = Tk()
    DVisual(root)
    root.mainloop()
