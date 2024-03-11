import numpy as np
from numpy import asarray
from PIL import Image
import os

from fade import FadeGenerator
from morph1 import Morph1Generator

if __name__ == "__main__":
    st = os.path.join("images","image10040.png")
    end = os.path.join("images","image10448.png")
    video_path = "hey.mp4"
    video_duration = 10
    video_fps = 24
    # fader = FadeGenerator(st, end, video_fps, video_path, video_duration)
    # fader.generate_conversion()
    morpher = Morph1Generator(st, end, video_fps, video_path, video_duration)
    morpher.generate_conversion()
    