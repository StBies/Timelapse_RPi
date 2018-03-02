# Timelapse videos using the PiCamera

import picamera
import time
import subprocess
import re #regular expressions
import os

VIDEO_RESOLUTION = (1920,1080)
CAPTURE_MINUTES = 1
FRAMES_PER_MIN = 24
FRAMES = FRAMES_PER_MIN * CAPTURE_MINUTES

def capture_frame(frame,cam):
    cam.capture('frame%04d.jpg' % frame)

def check_beginning_frame():
    dir_content = os.listdir()
    frame_numbers = []
    for element in dir_content:
        match = re.search("frame\d{4}.jpg",element)
        if match:
            number_match = re.search("\d{4}",match.group(0))
            frame_numbers.append(int(number_match.group(0)))
    frame_numbers.sort()
    if len(frame_numbers) > 0:
        return frame_numbers.pop()
    else:
        return 0

beginning_frame = check_beginning_frame()
print("Beginning with frame {}".format(beginning_frame))
#exit()
    

cam = picamera.PiCamera()
cam.resolution = VIDEO_RESOLUTION
time.sleep(2)
for frame in range(beginning_frame,FRAMES+beginning_frame):
    start = time.time()
    capture_frame(frame,cam)
    sleeptime = 60 / FRAMES_PER_MIN - (time.time() - start)
    print(sleeptime)
    if sleeptime < 0:
        sleeptime = 0.0
    time.sleep(sleeptime)
    
subprocess.call([
    'avconv', '-y',
    '-f', 'image2',
    '-i', 'frame%04d.jpg',
    '-r', '24',
    '-vcodec', 'libx264',
    '-profile', 'high',
    '-preset', 'slow',
    'timelapse.mp4',])
