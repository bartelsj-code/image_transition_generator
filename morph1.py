import numpy as np
from numpy import asarray
from PIL import Image
import os
import math

from convertion_generator import ConversionGenerator

class MPixel:
    def __init__(self, x, y, color, morph_radius, img_width, img_height):
        self.x = x
        self.y = y
        self.color = color
        self.m1 = 1
        self.m2 = 1
        self.morph_radius = morph_radius
        self.img_width = img_width
        self.img_height = img_height
        self.max_distance = math.sqrt(2*morph_radius**2)
        self.priorities = {}

    def get_color_distance(self, other_pixel):
        return sum(abs(self.color - other_pixel.color))

    def get_l2_distance(self, other_pixel):
        return math.sqrt((self.x - other_pixel.x)**2 + (self.y - other_pixel.y)**2)
    
    def get_color_closeness(self, other_pixel):
        return 1-(self.get_color_distance(other_pixel)/765)
    
    def get_l2_closeness(self, other_pixel):
        return 1-(self.get_l2_distance(other_pixel)/self.max_distance)
    
    def get_value(self, other_pixel):
        p1 = self.get_color_closeness(other_pixel)
        p2 = self.get_l2_closeness(other_pixel)
        value = self.m1*p1 + self.m2*p2**2
        return value
    
    def set_priorities(self, pixel_list_2d):
        low_x = max(0, self.x - self.morph_radius)
        high_x = min(self.img_width, self.x + self.morph_radius + 1)
        low_y = max(0, self.y - self.morph_radius)
        high_y = min(self.img_height, self.y + self.morph_radius + 1)
        amt = 0
        for x in range(low_x, high_x):
            for y in range(low_y, high_y):
                other_pixel = pixel_list_2d[x][y]
                value = self.get_value(other_pixel)
                self.priorities[other_pixel] = value
                other_pixel.priorities[self] = value


    def __repr__(self):
        return (f"({self.x},{self.y})")

class Morph1Generator(ConversionGenerator):
    def __init__(self, start_image_path, end_image_path, frame_count, video_path, duration):
        super().__init__(start_image_path, end_image_path, frame_count, video_path, duration)
        self.morph_radius = 4

    def generate_frames(self):
        width, height, channels = self.start_arr.shape
        start_pixels = []
        end_pixels = []
        for x in range(width):
            start_row = []
            end_row = []
            for y in range(height):
                pixel1 = MPixel(x, y, self.start_arr[x][y].astype(np.int16), self.morph_radius, width, height)
                pixel2 = MPixel(x, y, self.end_arr[x][y].astype(np.int16), self.morph_radius, width, height)
                start_row.append(pixel1)
                end_row.append(pixel2)
            start_pixels.append(start_row)
            end_pixels.append(end_row)
        i = 0
        l1 = len(start_pixels[0])
        l2 = len(start_pixels)
        for y in range(l1):
            for x in range(l2):
                start_pixels[x][y].set_priorities(end_pixels)
                i += 1
                if i % 1000 == 0:
                    print(f'{i}/{l1*l2} done', end = '\r')
        
        return None

    
    def generate_conversion(self):
        self.generate_frames()
        