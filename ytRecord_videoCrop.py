import pafy
import cv2
import time
import os
import sys
from datetime import datetime
import shutil

outDir = '/home/fatih/workspace/youtubeStreamRecord/cams/cam11/cam22_/'

camTxt = open('/home/fatih/workspace/youtubeStreamRecord/youtubeStrCam_v3.txt', 'r')

lines = camTxt.readlines()
folders = os.listdir(outDir)
frmNum = 1800
for count, line in enumerate(lines):
    commState = line.split(' ')[0]
    if commState != '#':
        camID = line.split(' ')[0]
        camURL = line.split(' ')[1]
        x1, y1, x2, y2 = line.split(' ')[2:6]  # crop coordinates
        resolution = line.split(' ')[6]
        width = int(resolution.split('x')[0])
        height = int(resolution.split('x')[1])
        fps = line.split(' ')[7]
        print('CamID: {}, URL: {}, x1,y1,x2,y2: {},{},{},{}, res: {}, fps: {}'.format(camID, camURL, x1, y1, x2, y2,
                                                                                      resolution, fps))
        vids = os.listdir(outDir)
        print(vids)
        for vid in vids:
            capTime = vid.split('.')[0]
            inputVid = outDir + vid
            outputVid = outDir + 'converted/cam{}_{}.mp4'.format(camID, capTime)
            cmd_str = "ffmpeg -i {} -vf \"crop={}:{}:{}:{},scale={}:{}\" -c:v libx264 -preset slow -crf 18 -an {}".format(inputVid, int(x2)-int(x1), int(y2)-int(y1), int(x1), int(y1), width, height, outputVid)
            os.system(cmd_str)
            # os.remove(inputVid)
            print('cam{} OK! {}'.format(camID, capTime))