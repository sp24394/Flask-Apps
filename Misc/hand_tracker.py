#!/usr/bin/env python3
"""
Real-time hand tracking with joint dots + connecting lines.
Uses MediaPipe's new Tasks API (mediapipe >= 1.0).

Usage: python hand_tracker.py [camera_index]
Press 'q' to quit.
"""

import os
import sys
import time
import urllib.request

import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks.python import BaseOptions
from mediapipe.tasks.python.vision import (
    HandLandmarker,
    HandLandmarkerOptions,
    RunningMode,
)

MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hand_landmarker.task")
MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/hand_landmarker/"
    "hand_landmarker/float16/1/hand_landmarker.task"
)

def ensure_model():
    if not os.path.exists(MODEL_PATH):
        print("Downloading hand landmark model (one-time, ~7MB)...")
        urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
        print("Done.")


# Landmark indices for thumb tip and index fingertip.
THUMB_TIP = 4
INDEX_TIP = 8

MAGENTA_BGR = (220, 0, 255)  # hex FF00DC -> RGB(255,0,220) -> BGR
BLACK_BGR = (0, 0, 0)
STRIPE_SIZE = 28  # pixels per stripe band, in screen space


def true_handedness(label):
    """The frame is mirrored for a selfie view, so MediaPipe's handedness
    (computed on the mirrored image) is the opposite of the person's actual
    hand."""
    return "Right" if label == "Left" else "Left"


def draw_bridge_polygon(frame, right_thumb, right_index, left_index, left_thumb):
    h, w = frame.shape[:2]
    polygon = np.array([right_thumb, right_index, left_index, left_thumb], dtype=np.int32)

    x, y, bw, bh = cv2.boundingRect(polygon)
    x0, y0 = max(x, 0), max(y, 0)
    x1, y1 = min(x + bw, w), min(y + bh, h)
    if x1 <= x0 or y1 <= y0:
        return

    mask = np.zeros((y1 - y0, x1 - x0), dtype=np.uint8)
    shifted = polygon - [x0, y0]
    cv2.fillPoly(mask, [shifted], 255)

    # Build the stripe pattern in *screen-space* coordinates (not local to
    # the bounding box), so the texture stays fixed in place while the
    # polygon window moves over it.
    yy, xx = np.indices((y1 - y0, x1 - x0))
    gx = xx + x0
    gy = yy + y0
    checker = ((gx // STRIPE_SIZE) + (gy // STRIPE_SIZE)) % 2

    magenta = np.array(MAGENTA_BGR, dtype=np.uint8)
    black = np.array(BLACK_BGR, dtype=np.uint8)
    pattern = np.where(checker[..., None] == 0, magenta, black).astype(np.uint8)

    region = frame[y0:y1, x0:x1]
    lit = mask > 0
    region[lit] = pattern[lit]


def draw_hand_bridge(frame, hand_landmarks, handedness, w, h):
    """If both a left and right hand are visible, draw a polygon bridging
    their thumb and index fingertips."""
    tips = {}
    for landmarks, hand_info in zip(hand_landmarks, handedness):
        label = true_handedness(hand_info[0].category_name)
        thumb = landmarks[THUMB_TIP]
        index = landmarks[INDEX_TIP]
        tips[label] = {
            "thumb": (int(thumb.x * w), int(thumb.y * h)),
            "index": (int(index.x * w), int(index.y * h)),
        }

    if "Left" in tips and "Right" in tips:
        draw_bridge_polygon(
            frame,
            tips["Right"]["thumb"],
            tips["Right"]["index"],
            tips["Left"]["index"],
            tips["Left"]["thumb"],
        )


def main():
    ensure_model()

    cam_index = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    cap = cv2.VideoCapture(cam_index, cv2.CAP_V4L2)
    if not cap.isOpened():
        print(f"Could not open camera index {cam_index}. "
              f"Try `v4l2-ctl --list-devices` (pkg: v4l-utils) for other indices.")
        sys.exit(1)

    options = HandLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=MODEL_PATH),
        running_mode=RunningMode.VIDEO,
        num_hands=2,
        min_hand_detection_confidence=0.6,
        min_tracking_confidence=0.6,
    )

    with HandLandmarker.create_from_options(options) as landmarker:
        start_time = time.time()
        while True:
            ok, frame = cap.read()
            if not ok:
                print("Failed to read frame from camera.")
                break

            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
            timestamp_ms = int((time.time() - start_time) * 1000)

            result = landmarker.detect_for_video(mp_image, timestamp_ms)

            h, w, _ = frame.shape
            if result.hand_landmarks and result.handedness:
                draw_hand_bridge(frame, result.hand_landmarks, result.handedness, w, h)

            cv2.imshow("Hand Tracking (q to quit)", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()