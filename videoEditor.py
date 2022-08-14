
import numpy as np
import cv2
from matplotlib.pyplot import savefig
from pytube import YouTube
from pytube import Playlist
from pytube import Channel
import os
import re
import subprocess
import ffmpeg

from cleantext import clean
from time import sleep


def get_length_of_video(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    return float(result.stdout)


def remove5secondsFromVideo(VideoPATH="", folderToUse="", secondsToRemove=0):
    """
    remove seconds from start
    """

    vidSeconds = get_length_of_video(VideoPATH)

    h = int(vidSeconds // 3600)
    m = int(vidSeconds // 60)
    s = secondsToRemove  # int(vidSeconds % 60) - 5

    if(h < 10):
        h = "0"+str(h)
    if(m < 10):
        m = "0"+str(m)
    if(s < 10):
        s = "0"+str(s)

    path_To_clipped_video = folderToUse+"\\"+"clippedVideo.mp4"

    # clear path to save video
    if os.path.exists(path_To_clipped_video):
        os.remove(path_To_clipped_video)

    #cmd = f'ffmpeg -ss 00:00:5 -to {h}:{m}:{s} -i "{VideoPATH}" -map 0 -c copy "{path_To_clipped_video}"'

    cmd = f'ffmpeg -ss 00:00:{s} -i {VideoPATH} {path_To_clipped_video}'

    subprocess.call(cmd, shell=True)
    return path_To_clipped_video


def flipVideo(VideoPATH="", AudioPATH="", folderToUse="", secondsToRemove=0):
    """
    return path_to_flipped_video
    """
    PATH_to_downloaded_video = VideoPATH
    PATH = folderToUse
    PATH_to_flipped_video = PATH+"\\"+"flippedVideo.mp4"

    PATH_to_clipped_video = remove5secondsFromVideo(
        VideoPATH, folderToUse, secondsToRemove)

    # clear path to flip video horizontally
    if os.path.exists(PATH_to_flipped_video):
        os.remove(PATH_to_flipped_video)

    # input downloaded video
    stream = ffmpeg.input(PATH_to_clipped_video)
    stream = ffmpeg.hflip(stream)
    stream = ffmpeg.output(stream, PATH_to_flipped_video)
    ffmpeg.run(stream)

    print("successfully flipped video check in: ", PATH_to_flipped_video)

    return PATH_to_flipped_video

    #remove flipped file and downloaded audio and video
    #if os.path.exists(PATH_to_downloaded_video):
    #    os.remove(PATH_to_downloaded_video)


def addMusic(VideoPATH="", AudioPATH="", folderToUse=""):
    """
    return path_to_final_video
    """
    PATH_to_flipped_video = VideoPATH
    PATH_to_downloaded_Audio = AudioPATH

    PATH = folderToUse

    # generated video path
    PATH_to_final_video = PATH + "\\"+"video.mkv"

    # clear path for final video
    if os.path.exists(PATH_to_final_video):
        os.remove(PATH_to_final_video)

    # add music to flipped video
    cmd = "ffmpeg -i "+VideoPATH+" -i "+AudioPATH + \
        " -map 0:v -map 1:a -c:v copy -shortest "+PATH_to_final_video

    subprocess.run(cmd)

    sleep(15)

    print("Added music successfully!")

    #remove flipped file and downloaded audio
    #if os.path.exists(PATH_to_flipped_video):
    #    os.remove(PATH_to_flipped_video)

    #if os.path.exists(PATH_to_downloaded_Audio):
    #    os.remove(PATH_to_downloaded_Audio)

    return PATH_to_final_video


def resizeVideo(VideoPATH="", AudioPATH="NONE", folderToUse=""):
    """
    return path_to_resized_video
    """
    PATH_to_flipped_video = VideoPATH
    PATH_to_downloaded_Audio = AudioPATH
    PATH = folderToUse

    # generated video path
    PATH_to_resized_video = PATH + "\\"+"resizedvideo.mkv"

    # clear path for final video
    if os.path.exists(PATH_to_resized_video):
        os.remove(PATH_to_resized_video)

    # Open the video
    cap = cv2.VideoCapture(PATH_to_flipped_video)

    # Initialize frame counter
    cnt = 0

    # Some characteristics from the original video
    w_frame, h_frame = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(
        cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps, frames = cap.get(cv2.CAP_PROP_FPS), cap.get(cv2.CAP_PROP_FRAME_COUNT)

    # Here you can define your croping values
    x, y, h, w = 0, 0, h_frame, w_frame

    # output
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(PATH_to_resized_video, fourcc, fps, (w, h))

    # Now we start
    while(cap.isOpened()):
        ret, frame = cap.read()

        cnt += 1  # Counting frames

        # Avoid problems when video finish
        if ret == True:
            # Croping the frame
            crop_frame = frame[y:y+h, x:x+w]

            # Percentage
            xx = cnt * 100/frames
            print(int(xx), '%')

            # Saving from the desired frames
            #if 15 <= cnt <= 90:
            #    out.write(crop_frame)

            # I see the answer now. Here you save all the video
            out.write(crop_frame)

            # Just to see the video in real time
            cv2.imshow('frame', frame)
            cv2.imshow('croped', crop_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    #addMusic("C:\\Users\\HP\\Desktop\\YT_video_projects\\project3\\flippedVideo.mp4", "C:\\Users\\HP\\Desktop\\YT_video_projects\\project3\\zABLecsR5UE.mp3", "C:\\Users\\HP\\Desktop\\YT_video_projects\\project3")
    #resizeVideo("C:\\Users\\HP\\Desktop\\YT_video_projects\\project1\\Video.mkv", "", "C:\\Users\\HP\\Desktop\\YT_video_projects\\project1")
    flipVideo("C:\\Users\\HP\\Desktop\\YT_video_projects\\projectt\\xh3nGdZa1ZI.mp4",
              "", "C:\\Users\\HP\\Desktop\\YT_video_projects\\projectt", 24)


