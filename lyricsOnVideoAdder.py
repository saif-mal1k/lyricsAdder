import json
import subprocess
import os
import re

from time import sleep

from cleantext import clean


def clean_text(title):
    title = clean(title, no_emoji=True)
    save_title = str(title)
    to_replace = {'/': '', ':': '', '*': '',
                  '?': '', '"': '', '<': '', '>': '', '|': ''}
    save_title = re.sub(
        r'[\/:*?"<>|]', lambda x: to_replace[x.group(0)], save_title)
    save_title = save_title.replace("'", "")
    #save_title = save_title.replace(",", "")
    save_title = save_title.replace("(", "")
    save_title = save_title.replace(")", "")
    save_title = save_title.replace("♪", "")
    return save_title


def thsecond(startTime):
    """
    when start time in miliseconds is given, this function converts it to seconds
    """
    seconds = (int(startTime)/1000)
    if (seconds < 60):
        seconds = seconds % 60
    else:
        mult = seconds//60
        #print(mult)
        seconds = seconds % 60
        seconds = seconds+60*(mult)

    sec = int(seconds)

    return sec


def thsecond2(startTime="0:00"):
    """
    when start time in 0:00 format is given, this function converts it to seconds
    """
    listt = startTime.split(':')
    seconds = int(listt[0])*60 + int(listt[1])
    return seconds



def addSpotifyLyrics(path_to_music_video, path_to_lyrics_file, folder_to_use):

    # Opening JSON file
    filee = open(path_to_lyrics_file)

    # returns JSON object as
    # a dictionary
    data = json.load(filee)

    # Iterating through the json
    # list
    lines = data['lyrics']['lines']

    # "drawtext=fontfile=font4.ttf:text='...':fontcolor=white:fontsize=90:box=1:boxcolor=black@0.5:boxborderw=5:x=(w-text_w)/2:y=h-th-180:enable='between(t,0,0)'"
    subtitles = f'drawtext=fontfile=font4.ttf:text=\'...\':fontcolor=white:fontsize=90:box=1:boxcolor=black@0.5:boxborderw=5:x=(w-text_w)/2:y=h-th-180:enable=\'between(t,0,1)\''

    i = 0
    while(i < len(lines)):
        #print(len(lines))
        #print(i)
        #print(lines[i])
        del lines[i]['syllables']

        startTimeMs = lines[i]['startTimeMs']

        startTime = thsecond(startTimeMs)

        lines[i]['startTimeMs'] = startTime

        if(i < (len(lines)-1)):
            endTimeMs = lines[i+1]['startTimeMs']
            endTime = thsecond(endTimeMs)
            lines[i]['endTimeMs'] = endTime

        else:
            endTime = startTime+2
            lines[i]['endTimeMs'] = endTime

        words = lines[i]['words']

        words = clean_text(words)
        print(words)

        # if there are more than 5 words, split them into multiple lines
        if(len(words.split(' ')) > 6):
            list_of_words = words.split(' ')

            # add initial five words to the first line
            str1 = " "
            initial_five_Words = str1.join(list_of_words[:6])

            subtitles += f' , drawtext=fontfile=font4.ttf:text=\'{initial_five_Words}\':fontcolor=white:fontsize=75:box=1:boxcolor=black@0.5:boxborderw=5:x=(w-text_w)/2:y=h-th-180:enable=\'between(t,{startTime},{endTime})\''

            # add the rest of the words to the second line
            str2 = " "
            rest_of_words = str2.join(list_of_words[6:])

            subtitles += f' , drawtext=fontfile=font4.ttf:text=\'{rest_of_words}\':fontcolor=white:fontsize=75:box=1:boxcolor=black@0.5:boxborderw=5:x=(w-text_w)/2:y=h-th-100:enable=\'between(t,{startTime},{endTime})\''
        else:
            subtitles += f' , drawtext=fontfile=font4.ttf:text=\'{words}\':fontcolor=white:fontsize=75:box=1:boxcolor=black@0.5:boxborderw=5:x=(w-text_w)/2:y=h-th-180:enable=\'between(t,{startTime},{endTime})\''

        i += 1

    print("\n#######################################################################\n")

    #for line in lines:
    #    print(line)
    #
    #print(subtitles)

    #drawtext=fontfile=font4.ttf:text='Stack Overflow Answers are the best site where developers help developers':fontcolor=white:fontsize=90:box=1:boxcolor=black@0.5:boxborderw=5:x=(w-text_w)/2:y=h-th-180:enable='between(t,8,15)'

    PATH_for_present_video = folder_to_use + "\\" + 'final.mkv'

    # clear path to store present video
    if os.path.exists(PATH_for_present_video):
        os.remove(PATH_for_present_video)

    cmd = f'ffmpeg -i {path_to_music_video} -vf "[in] {subtitles} [out]" -codec:a copy  {PATH_for_present_video}'

    print(cmd)

    subprocess.run(cmd)

    sleep(10)

    # Closing file
    filee.close()


def ytTranscriptToJSON(transcript="transcript.txt"):
    """
    Converts a transcript to a JSON object.
    """

    # read line from links.txt
    with open(transcript, 'r') as filee:
        #get all text
        text = filee.read()

        listt = text.split('\n')

        #lines = filee.readlines()

    i = 0
    lines = []
    while(i < len(listt)):
        line = {}
        line['starttime'] = listt[i]
        line['words'] = listt[i+1]
        if(i+2 < len(listt)):
            line['endtime'] = listt[i+2]
        else:
            line['endtime'] = listt[i]

        lines.append(line)
        i += 2

    #print(lines)

    #close file
    filee.close()

    return lines


def addYoutubeLyrics(path_to_music_video, path_to_transcript_file, folder_to_use):

    lines = ytTranscriptToJSON(path_to_transcript_file)

    print(lines)

    subtitles = f'drawtext=fontfile=font4.ttf:text=\'...\':fontcolor=white:fontsize=90:box=1:boxcolor=black@0.5:boxborderw=5:x=(w-text_w)/2:y=h-th-180:enable=\'between(t,0,1)\''

    i = 0
    while(i < len(lines)):
        #print(len(lines))
        #print(i)
        #print(lines[i])

        words = lines[i]['words']

        words = clean_text(words)
        print(words)

        startTime = lines[i]['starttime']

        endTime = lines[i]['endtime']

        startTime = thsecond2(startTime)

        endTime = thsecond2(endTime)

        # if there are more than 5 words, split them into multiple lines
        if(len(words.split(' ')) > 6):
            list_of_words = words.split(' ')

            # add initial five words to the first line
            str1 = " "
            initial_five_Words = str1.join(list_of_words[:5])

            subtitles += f' , drawtext=fontfile=font4.ttf:text=\'{initial_five_Words}\':fontcolor=white:fontsize=65:box=1:boxcolor=black@0.5:boxborderw=5:x=(w-text_w)/2:y=h-th-180:enable=\'between(t,{startTime},{endTime})\''

            # add the rest of the words to the second line
            str2 = " "
            rest_of_words = str2.join(list_of_words[5:10])

            subtitles += f' , drawtext=fontfile=font4.ttf:text=\'{rest_of_words}\':fontcolor=white:fontsize=65:box=1:boxcolor=black@0.5:boxborderw=5:x=(w-text_w)/2:y=h-th-100:enable=\'between(t,{startTime},{endTime})\''

            # add the rest of the words to the second line
            str3 = " "
            rest_of_rest_words = str2.join(list_of_words[10:])

            subtitles += f' , drawtext=fontfile=font4.ttf:text=\'{rest_of_rest_words}\':fontcolor=white:fontsize=65:box=1:boxcolor=black@0.5:boxborderw=5:x=(w-text_w)/2:y=h-th-20:enable=\'between(t,{startTime},{endTime})\''


        else:
            subtitles += f' , drawtext=fontfile=font4.ttf:text=\'{words}\':fontcolor=white:fontsize=65:box=1:boxcolor=black@0.5:boxborderw=5:x=(w-text_w)/2:y=h-th-180:enable=\'between(t,{startTime},{endTime})\''

        i += 1

    print("\n#######################################################################\n")

    PATH_for_present_video = folder_to_use + "\\" + 'final.mkv'

    # clear path to store present video
    if os.path.exists(PATH_for_present_video):
        os.remove(PATH_for_present_video)

    cmd = f'ffmpeg -i {path_to_music_video} -vf "[in] {subtitles} [out]" -codec:a copy  {PATH_for_present_video}'

    print(cmd)

    subprocess.run(cmd)

    sleep(10)


if __name__ == '__main__':
    addYoutubeLyrics('C:\\Users\\HP\\Desktop\\YT_video_projects\\projectt\\video.mkv',
              'C:\\Users\\HP\\Desktop\\YT_video_projects\\project4\\transcript.txt', 'C:\\Users\\HP\\Desktop\\YT_video_projects\\project4')
