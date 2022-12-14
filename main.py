import AudioVideoDownloader

import os

import videoEditor

import lyricsDownloader

import lyricsOnVideoAdder

from time import sleep


def create_dir(folder_name='YT_video_projects', projectName=''):
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    PATH = f'{desktop}\\{folder_name}\\{projectName}'
    os.makedirs(PATH, exist_ok=True)
    return PATH
    



if __name__ == '__main__':

    #lyricsToDownload = "https://open.spotify.com/track/6HMtHNpW6YPi1hrw9tgF8P"

    audioToDownload = "https://www.youtube.com/watch?v=Tuwmzdneass"

    videoToDownload = "https://www.youtube.com/watch?v=BvOT6L5yVK8"

    projectName = "project4"

    PATH = create_dir('YT_video_projects', projectName)

    path_to_yt_lyrics = f'{PATH}\\transcript.txt'
    #path_to_spotify_lyrics = lyricsDownloader.lyricsDownload(lyricsToDownload, PATH)

    sleep(18)
    
    path_to_downloaded_audio, Save_title = AudioVideoDownloader.download160kbpsAudio(audioToDownload,PATH)
    path_to_downloaded_video, video_title = AudioVideoDownloader.download1080pVideo(videoToDownload,PATH)

    sleep(16)

    path_to_flipped_video = videoEditor.flipVideo(path_to_downloaded_video,path_to_downloaded_audio, PATH, 0)
    path_to_music_video = videoEditor.addMusic(path_to_flipped_video, path_to_downloaded_audio, PATH)

    sleep(10)

    sleep(12)

    path_to_final_video = lyricsOnVideoAdder.addYoutubeLyrics(path_to_music_video, path_to_yt_lyrics, PATH)
    #path_to_final_video = lyricsOnVideoAdder.addSpotifyLyrics(path_to_music_video, path_to_spotify_lyrics, PATH)





