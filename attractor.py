#!/usr/bin/env python
import os
import sys
import time
import threading
from Tkinter import *

from image import AttractorImage

a = 2.0
b = 2.0
c = 2.0
d = 2.0
resolution = 1
intensity = 0.95

attrs = ['a', 'b', 'c', 'd', 'intensity', 'resolution']

class Display:
    render_flag = False

    def __init__(self, master):
        self.attractor = AttractorImage()
        self.attractor.render(0.1)

        frame = Frame(master)
        frame.grid(row=0, column=0)
        self.frame = frame

        Label(frame, text="a:").grid(row=0, column=0, sticky=E)
        Label(frame, text="b:").grid(row=0, column=2, sticky=E)
        Label(frame, text="c:").grid(row=1, column=0, sticky=E)
        Label(frame, text="d:").grid(row=1, column=2, sticky=E)
        Label(frame, text="Resolution:").grid(row=2, column=0, sticky=E)
        Label(frame, text="Intensity:").grid(row=3, column=0, sticky=E)
	self.iterations_label = Label(frame, text="Iterations: ")
	self.iterations_label.grid(row=4, column=0)

        self.a_entry = Entry(frame)
        self.b_entry = Entry(frame)
        self.c_entry = Entry(frame)
        self.d_entry = Entry(frame)
        self.resolution_entry = Entry(frame)
        self.intensity_entry = Entry(frame)

        self.a_entry.insert(0, a)
        self.b_entry.insert(0, b)
        self.c_entry.insert(0, c)
        self.d_entry.insert(0, d)
        self.resolution_entry.insert(0, resolution)
        self.intensity_entry.insert(0, intensity)

        self.a_entry.grid(row=0, column=1)
        self.b_entry.grid(row=0, column=3)
        self.c_entry.grid(row=1, column=1)
        self.d_entry.grid(row=1, column=3)        
        self.resolution_entry.grid(row=2, column=1)
        self.intensity_entry.grid(row=3, column=1)        

        attractor_img = self.attractor.get_photo_image(512, 512)
        self.image_canvas = Canvas(frame, width=512, height=512)
        self.image_canvas.image = attractor_img
        self.image_canvas.create_image((0,0),
                                       {'image': attractor_img,
                                        'anchor': NW})
        self.image_canvas.grid(row=0, column=4,
                               padx=5, pady=5,
                               sticky=W+E+N+S,
                               rowspan=5)

        self.render_button = Button(frame,
                                    text="Render",
                                    command=self.toggle_render)
        self.render_button.grid(row=5, column=3)
        
        self.exit_button = Button(frame, text="Exit", command=self.quit)
        self.exit_button.grid(row=5, column=4)

        self.running = True
        self.render_thread = threading.Thread(target=self.worker_thread)

    def quit(self):
        self.render_flag = False
        self.running = False
        self.frame.quit()
        
    def toggle_render(self):
        if self.render_flag:
            self.render_flag = False
            self.render_button["text"] = "Render"
        else:
            self.update_attractor()
            self.render_flag = True
            self.render_button["text"] = "Pause"

    def worker_thread(self):
        while self.running:
            if self.render_flag:
                self.attractor_render(0.05)
                self.iterations_label["text"] = "Iterations: %s" % self.attractor.iterations
            else:
                time.sleep(0.05)
                

    def attractor_render(self, duration):
        self.attractor.render(duration)

        attractor_img = self.attractor.get_photo_image(512, 512)
        self.image_canvas.delete(ALL)
        self.image_canvas.image = attractor_img
        self.image_canvas.create_image((0,0),
                                       {'image': attractor_img,
                                        'anchor': NW})

    def update_attractor(self):
        # Update values from textboxes, see if we need 
        # to re-initialize the image
        try:
            for attr in attrs:
                if str(getattr(self.attractor, attr)) != getattr(self, attr+'_entry').get():
                    self.attractor = AttractorImage(
                        resolution = int(self.resolution_entry.get()),
                        intensity = float(self.intensity_entry.get()),
                        a = float(self.a_entry.get()),
                        b = float(self.b_entry.get()),
                        c = float(self.c_entry.get()),
                        d = float(self.d_entry.get()))

        except ValueError():
            return

    
root = Tk()
display = Display(root)
display.render_thread.start()

root.mainloop()

