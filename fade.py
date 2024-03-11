import numpy as np
from numpy import asarray
from PIL import Image
import os

from convertion_generator import ConversionGenerator

class FadeGenerator(ConversionGenerator):
    def __init__(self, start_image_path, end_image_path, frame_count, video_path, duration):
        super().__init__(start_image_path, end_image_path, frame_count, video_path, duration)

    def generate_frames(self):
        # delta = (self.end_arr - self.start_arr).astype(np.int8)
        # step = delta/self.frame_count
        # print(step)
        frames_out = []
        # frames = [self.start_arr]
        for i in range(self.frame_count):
            print(f'generating frame: {i}', end = '\r')
            # result = frames[-1] + step
            ratio = i/self.frame_count
            start_multiplier = ratio
            end_multiplier = 1-ratio
            start_part = self.start_arr * start_multiplier
            end_part = self.end_arr * end_multiplier
            result = start_part + end_part
            frames_out.append(np.round(result).astype(np.uint8))
            # frames.append(result)
        print()
        return frames_out
