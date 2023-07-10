import tqdm
# This reads frames from source video and writes the processed frames to the output video
from supervision.video.dataclasses import VideoInfo
from supervision.video.sink import VideoSink
from supervision.video.source import get_video_frames_generator
from supervision.tools.detections import Detections, BoxAnnotator
from supervision.draw.color import ColorPalette
from supervision.tools.line_counter import LineCounter, LineCounterAnnotator

from ultralytics import YOLO
# pip install bytetracker
# necessary to use counting

# pip install supervision==0.1.0
# necessary to use counting

# Load a model
model = YOLO('yolov8n.pt')  # load an official detection model
#model.fuse() # necessary for counting
CLASS_NAMES_DICT = model.names

box_annotator = BoxAnnotator(color=ColorPalette(), thickness=4, text_thickness=4, text_scale=2)

video_info = VideoInfo.from_video_path('IMG_2022.mov')

frame_generator = get_video_frames_generator('IMG_2022.mov')


#tracking code
from typing import List

import numpy as np


# converts Detections into format that can be consumed by match_detections_with_tracks function
def detections2boxes(detections: Detections) -> np.ndarray:
    return np.hstack((
        detections.xyxy,
        detections.confidence[:, np.newaxis]
    ))


# converts List[STrack] into format that can be consumed by match_detections_with_tracks function
def tracks2boxes(tracks: List[STrack]) -> np.ndarray:
    return np.array([
        track.tlbr
        for track
        in tracks
    ], dtype=float)


# matches our bounding boxes with predictions
def match_detections_with_tracks(
    detections: Detections,
    tracks: List[STrack]
) -> Detections:
    if not np.any(detections.xyxy) or len(tracks) == 0:
        return np.empty((0,))

    tracks_boxes = tracks2boxes(tracks=tracks)
    iou = box_iou_batch(tracks_boxes, detections.xyxy)
    track2detection = np.argmax(iou, axis=1)

    tracker_ids = [None] * len(detections)

    for tracker_index, detection_index in enumerate(track2detection):
        if iou[tracker_index, detection_index] != 0:
            tracker_ids[detection_index] = tracks[tracker_index].track_id

    return tracker_ids

with VideoSink('./runs/supervision_test.mp4', video_info) as sink:
    for frame in tqdm.tqdm(frame_generator, total=video_info.total_frames):
        results = model(frame)[0]

        #print(results.boxes.xyxy)

        detections = Detections(
            xyxy=results.boxes.xyxy.cpu().numpy(),
            confidence=results.boxes.conf.cpu().numpy(),
            class_id=results.boxes.cls.cpu().numpy().astype(int)
        )

        labels = [f"{CLASS_NAMES_DICT[class_id]} {confidence:0.2f}" for _, confidence, class_id, tracker_id in detections]

        frame = box_annotator.annotate(frame=frame, detections=detections, labels=labels)

        sink.write_frame(frame)

"""

with VideoSink('./runs/supervision_test.mp4', video_info) as sink:
    for frame in tqdm(generator, total=video_info.total_frames):
        frame = ...
        sink.write_frame(frame)
        
 
 # This counts how many detections cross a virtual line       
from supervision.tools.line_counter import LineCounter
from supervision.geometry.dataclasses import Point

LINE_START = Point(50, 1500) # set coordinates of start point
LINE_END = Point(3790, 1500) # set coordinates of end point

line_counter = LineCounter(start=LINE_START, end=LINE_END)

for frame in frames:
    detections = ...
    line_counter.update(detections=detections)
    


# Track with the model
results = model.track(source="vid2.mov", save=True) 
#results = model.track(source="https://youtu.be/Zgi9g1ksQHc", show=True, tracker="bytetrack.yaml") 
"""