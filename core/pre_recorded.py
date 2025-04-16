import os
import random
import pygame
from config import clips_dir, mclovin_triggers

def play_clip(keyword):
    if keyword in mclovin_triggers:
        clip_name = random.choice(mclovin_triggers[keyword])
        clip_path = os.path.join(clips_dir, clip_name)
        if os.path.exists(clip_path):
            pygame.mixer.init()
            pygame.mixer.music.load(clip_path)
            pygame.mixer.music.play()
        else:
            print(f"Clip not found: {clip_path}")
