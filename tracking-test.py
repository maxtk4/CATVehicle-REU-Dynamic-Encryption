from ultralytics import YOLO
# pip install bytetracker
# necessary to use counting

# pip install supervision==0.1.0
# necessary to use counting

# Load a model
model = YOLO('yolov8n.pt')  # load an official detection model
#model.fuse() # necessary for counting
#model = YOLO('yolov8n-seg.pt')  # load an official segmentation model
#model = YOLO('path/to/best.pt')  # load a custom model



#Predict
detections = model(frame)


# This reads frames from source video and writes the processed frames to the output video
from supervision.video.dataclasses import VideoInfo
from supervision.video.sink import VideoSink
from supervision.video.source import get_video_frames_generator

video_info = VideoInfo.from_video_path(SOURCE_VIDEO_PATH)

generator = get_video_frames_generator(SOURCE_VIDEO_PATH)

with VideoSink(TARGET_VIDEO_PATH, video_info) as sink:
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