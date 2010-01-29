import time
import math
import Image
import ImageTk
import random

class AttractorImage():
    def __init__(self, resolution=1, dimension=256, intensity=0.95,
                 a=2.0, b=2.0, c=2.0, d=2.0):
        self.intensity = intensity
        self.resolution = resolution
        self.dimension = dimension
        width = dimension*self.resolution
        height = dimension*self.resolution
        self.x_origin = width/2
        self.y_origin = height/2
        self.x_scale = 50*resolution
        self.y_scale = 50*resolution

        self.im = Image.new("RGB",
                            (width, height),
                            (255, 255, 255))

        self.curpoint = [random.randrange(-2.0, 2.0),
                         random.randrange(-2.0, 2.0)]
        
        self.a = a
        self.b = b
        self.c = c
        self.d = d

        self.iterations = 0

    def attractor(self, x,y):
        x = math.sin(self.a*y)-math.cos(self.b*x)
        y = math.sin(self.c*x)-math.cos(self.d*y)
        return (x,y)

    def render(self, duration):
        start_time = time.time()
        pix = self.im.load()
        while((time.time() - start_time) < duration):
            self.curpoint = self.attractor(
                self.curpoint[0],
                self.curpoint[1])
            imgpoint = (self.x_origin+(self.curpoint[0]*self.x_scale),
                        self.y_origin+(self.curpoint[1]*self.y_scale))
            pix[imgpoint[0], imgpoint[1]] = (
                int(pix[imgpoint[0], imgpoint[1]][0]*self.intensity),
                int(pix[imgpoint[0], imgpoint[1]][1]*self.intensity),
                int(pix[imgpoint[0], imgpoint[1]][2]*self.intensity))
            self.iterations += 1

    def get_photo_image(self, x, y):
        return ImageTk.PhotoImage(self.im.resize((x,y), Image.ANTIALIAS))
