import pafy
import cv2
import time
import os
import sys
from datetime import datetime
import shutil

outDir = '/home/ubuntu/phd/youtubeStreamRecord/cams/'

# logF = '/home/fatih/mnt/datasets/MyDataset/youtubeStrCam_v3/ytRecord.log'


camTxt = open('/home/ubuntu/phd/youtubeStreamRecord/youtubeStrCam_v3.txt', 'r')

lines = camTxt.readlines()
frmNum = 600
for count, line in enumerate(lines):
    commState = line.split(' ')[0]
    if commState != '#':
        camID = line.split(' ')[0]
        camURL = line.split(' ')[1]
        x1, y1, x2, y2 = line.split(' ')[2:6]  # crop coordinates
        resolution = line.split(' ')[6]
        fps = line.split(' ')[7]
        print('CamID: {}, URL: {}, x1,y1,x2,y2: {},{},{},{}, res: {}, fps: {}'.format(camID, camURL, x1, y1, x2, y2,
                                                                                      resolution, fps))
        video = pafy.new(camURL)
        best = video.getbest(preftype="mp4")
        capture = cv2.VideoCapture(best.url)

        capTime = datetime.now().strftime('%Y-%m-%d,%H:%M:%S')
        if not os.path.exists(outDir + 'cam{}'.format(camID)):
            os.makedirs(outDir + 'cam{}'.format(camID))
        orgPath1 = outDir + 'cam{}/'.format(camID)
        orgPath2 = orgPath1 + '/img1'
        os.mkdir(orgPath2)
        inx = 1
        timeout = 0
        timeoutFlag = 0
        while inx <= frmNum:
            grabbed, frame = capture.read()
            if grabbed:
                cv2.imwrite(orgPath2 + '/img{:05d}.jpg'.format(inx), frame[int(y1):int(y2), int(x1):int(x2)])
                inx += 1
                timeout = 0
            timeout += 1
            if timeout == 1000000:
                shutil.rmtree(orgPath2)
                timeoutFlag = 1
                break
        if timeoutFlag == 1:
            print('cam{} timeout!!!'.format(camID))
            capture.release
            continue
        else:
            capture.release
            inputImg = orgPath2 + '/img%05d.jpg'
            outputVid = orgPath1 + '/img1.mp4'
            cmd_str = "ffmpeg -r 30 -i {} -c:v libx264 -vf fps=30 -pix_fmt yuv420p {}".format(inputImg, outputVid)
            print(cmd_str)
            os.system(cmd_str)
            newWidth = int(x2) - int(x1)
            newHeight = int(y2) - int(y1)
            if newWidth == 1920:
                shutil.rmtree(orgPath2)
                os.rename(outputVid, orgPath1 + '/cam' + camID + '_' + capTime)
                continue
            elif newWidth == 1280:
                shutil.rmtree(orgPath2)
                os.rename(outputVid, orgPath1 + '/cam' + camID + '_' + capTime)
                continue
            elif newWidth < 1280:
                cmd_str = "ffmpeg -i {} -vf scale=1280x720:flags=bicubic -c:v libx264 -preset slow -crf 18 {}.mp4".format(
                    outputVid, orgPath1 + '/cam' + camID + '_' + capTime)
            elif 1280 < newWidth < 1920:
                cmd_str = "ffmpeg -i {} -vf scale=1920x1080:flags=bicubic -c:v libx264 -preset slow -crf 18 {}.mp4".format(
                    outputVid, orgPath1 + '/cam' + camID + '_' + capTime)
            os.system(cmd_str)
            shutil.rmtree(orgPath2)
            os.remove(outputVid)
