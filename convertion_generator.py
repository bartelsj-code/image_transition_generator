import numpy as np
from numpy import asarray
from PIL import Image
import cv2
import os

class ConversionGenerator:
    def __init__(self, start_image_path, end_image_path, fps, video_path, duration):
        self.start_arr = self.image_to_np_array(start_image_path)
        self.end_arr = self.image_to_np_array(end_image_path)
        self.frame_count = duration * fps
        print("frame_count = ", self.frame_count)
        self.fps = fps
        self.video_path = video_path
        self.duration = duration

    def image_to_np_array(self, file_path):
        img = Image.open(file_path)
        np_arr = asarray(img)
        return np_arr

    def make_video(self, frames):
        height, width, layers = frames[0].shape
        video = cv2.VideoWriter(self.video_path, cv2.VideoWriter_fourcc(*'mp4v'), self.fps, (width, height))
        
        for i, frame in enumerate(frames):
            print(f"adding frame {i}", end = "\r")
            bgr_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            video.write(bgr_frame)
        video.release()


    def generate_conversion(self):
        frames = self.generate_frames()
        self.make_video(frames)
        
    def generate_frames(self):
        pass