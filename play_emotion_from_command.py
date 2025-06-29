# play_emotion_from_command.py

import socket
import numpy as np
import random

from livelink.connect.livelink_init import initialize_py_face, create_socket_connection
from utils.generated_runners import run_audio_animation
from livelink.animations.animation_loader import emotion_animations
from livelink.animations.animation_emotion import merge_emotion_data_into_facial_data_wrapper

def play_emotion(emotion_name: str):
    if emotion_name not in emotion_animations or not emotion_animations[emotion_name]:
        print(f"❌ Emotion '{emotion_name}' not found or empty.")
        return

    # Create neutral dummy base
    selected = random.choice(emotion_animations[emotion_name])
    dummy_base = np.zeros((len(selected), 68))  # 68 includes the 61 ARKit + 7 emotion weights

    # Merge emotion overlay
    with_emotion = merge_emotion_data_into_facial_data_wrapper(dummy_base.tolist(), selected)

    run_audio_animation(
        audio_input=None,
        generated_facial_data=with_emotion,
        py_face=initialize_py_face(),
        socket_connection=create_socket_connection(),
        default_animation_thread=None
    )
