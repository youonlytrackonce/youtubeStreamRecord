import pafy
import cv2
import time
import os
import sys
from datetime import datetime
import shutil

outDir = '/home/fatih/mnt/datasets/MyDataset/AllSeasons/cams_v4/'

camTxt = open('/home/fatih/workspace/youtubeStreamRecord/youtubeStrCam_v4.txt', 'r')

lines = camTxt.readlines()
frmNum = 1800
tAll = time.time()
for count, line in enumerate(lines):
    commState = line.split(' ')[0]
    if commState != '#':
        t1 = time.time()
        camID = line.split(' ')[0]
        camURL = line.split(' ')[1]
        x1, y1, x2, y2 = line.split(' ')[2:6]  # crop coordinates
        resolution = line.split(' ')[6]
        fps = line.split(' ')[7]
        print('CamID: {}, URL: {}, x1,y1,x2,y2: {},{},{},{}, res: {}, fps: {}'.format(camID, camURL, x1, y1, x2, y2,
                                                                                      resolution, fps))
        if not os.path.exists(outDir + 'cam{}'.format(camID)):
            os.makedirs(outDir + 'cam{}'.format(camID))
        orgPath1 = outDir + 'cam{}/'.format(camID)
        try:
            video = pafy.new(camURL)
            best = video.getbest(preftype="mp4")
            capture = cv2.VideoCapture(best.url)
        except Exception as ex:
            print(ex)
            continue

        frame_width = int(capture.get(3))
        frame_height = int(capture.get(4))
        out = cv2.VideoWriter(orgPath1 + 'outpy.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), int(fps), (frame_width, frame_height))
        capTime = datetime.now().strftime('%Y-%m-%d,%H:%M:%S')
        inx = 1
        timeout = 0
        timeoutFlag = 0
        while inx <= frmNum:
            grabbed, frame = capture.read()
            if grabbed:
                out.write(frame)
                inx += 1
                timeout = 0
            timeout += 1
            if timeout == 1000000:
                timeoutFlag = 1
                break
        capture.release()
        out.release()
        if timeoutFlag == 1:
            print('cam{} timeout!!! {} elapsed time: {}'.format(camID, capTime, time.time()-t1))
            os.remove(orgPath1 + 'outpy.avi')
            continue
        else:
            inputVid = orgPath1 + 'outpy.avi'
            outputVid = orgPath1 + 'cam{}_{}.mp4'.format(camID, capTime)
            cmd_str = "ffmpeg -i {} -vf \"crop={}:{}:{}:{},scale={}:{}\" -c:v libx264 -preset slow -crf 18 {}".format(inputVid, int(x2)-int(x1), int(y2)-int(y1), int(x1), int(y1), frame_width, frame_height, outputVid)
            os.system(cmd_str)
            os.remove(inputVid)
            print('cam{} OK! {} elapsed time: {}'.format(camID, capTime, time.time()-t1))
print('Total elapsed time: {}'.format(time.time()-tAll))
