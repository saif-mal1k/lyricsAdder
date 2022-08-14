from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep, strftime
from random import randint
import pandas as pd
import json

# Change this to your own chromedriver path!
Edgedriver_path = 'G:\\edgeDriver\\104\\msedgedriver.exe'
webdriver = webdriver.Edge(executable_path=Edgedriver_path)


def login():
    webdriver.get('https://open.spotify.com/')
    sleep(5)

    username = "***************"    #enter email id or username here
    password = "***************"    #enter password here
    sleep(10)

    login_button = webdriver.find_element_by_xpath("/html/body/div[3]/div/div[2]/div[1]/header/div[5]/button[2]").click()
    sleep(6)

    enter_email = webdriver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/div/div[2]/div[1]/input").send_keys(username)
    sleep(2)

    enter_password = webdriver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/div/div[2]/div[2]/input").send_keys(password)
    sleep(2)

    click_login = webdriver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/div/div[2]/div[3]/div[2]/button").click()
    sleep(14)

    try:
        webdriver.find_element_by_xpath("/html/body/div[14]/div[3]/div/div[2]/button").click()
    except:
        try:
            webdriver.find_element_by_xpath("/html/body/div[14]/div[3]/div/div[2]/button").click()
        except:
            pass
    sleep(4)


def logOut():
    webdriver.get('https://open.spotify.com/')
    sleep(5)

    right_drobdown_btn = webdriver.find_element_by_xpath("/html/body/div[4]/div/div[2]/div[1]/header/button[2]").click()

    sleep(4)

    logout_btn = webdriver.find_element_by_xpath("/html/body/div[4]/div/div[2]/div[1]/header/div[5]/div/div/ul/li[4]/button").click()

    sleep(5)

    webdriver.quit()
    

def open_playlist():
    webdriver.get('https://open.spotify.com/playlist/1yBsdsUwfFQOJWbvjyWxDc')
    sleep(10)

    # opened playlist
    first_song = webdriver.find_element_by_xpath('/html/body/div[4]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div/div/div[2]/main/div/section/div[2]/div[3]/div/div[2]/div[2]/div[1]/div/div[2]/div/a')
    first_song_url = first_song.get_attribute("href")


def open_song_on_url(first_song_url= 'https://open.spotify.com/track/48fKgzfvTU4U7eyRtIYaHP', PATH_for_json=""):
    # open first song
    webdriver.get(first_song_url)
    sleep(16)

    # remove popup
    try:
        webdriver.find_element_by_xpath(
            "/html/body/div[14]/div[3]/div/div[2]/button").click()
    except:
        try:
            webdriver.find_element_by_xpath(
                "/html/body/div[14]/div[3]/div/div[2]/button").click()
        except:
            pass
    sleep(4)

    # get track id
    try:
        track_id = webdriver.find_element_by_xpath('/html/head/meta[7]').get_attribute("content").replace("https://open.spotify.com/track/","")
    except:
        try:
           track_id = webdriver.find_element_by_xpath('/html/head/meta[7]').get_attribute("content").replace("https://open.spotify.com/track/", "")
        except:
            try:
                track_id = webdriver.find_element_by_xpath('/html/head/meta[7]').get_attribute("content").replace("https://open.spotify.com/track/", "")
            except:
                try:
                    track_id = webdriver.find_element_by_xpath('/html/head/meta[7]').get_attribute("content").replace("https://open.spotify.com/track/", "")
                except:
                    track_id = webdriver.find_element_by_xpath('/html/head/meta[7]').get_attribute("content").replace("https://open.spotify.com/track/", "")


    # get key
    try:
        track_key = webdriver.find_element_by_xpath('/html/head/meta[8]').get_attribute("content").replace("https://i.scdn.co/image/","")
    except:
        try:
            track_key = webdriver.find_element_by_xpath('/html/head/meta[8]').get_attribute("content").replace("https://i.scdn.co/image/", "")
        except:
            try:
                track_key = webdriver.find_element_by_xpath('/html/head/meta[8]').get_attribute("content").replace("https://i.scdn.co/image/", "")
            except:
                try:
                    track_key = webdriver.find_element_by_xpath('/html/head/meta[8]').get_attribute("content").replace("https://i.scdn.co/image/", "")
                except:
                    track_key = webdriver.find_element_by_xpath(
                        '/html/head/meta[8]').get_attribute("content").replace("https://i.scdn.co/image/", "")

    # predefined elements of url
    middle_code = "image/https%3A%2F%2Fi.scdn.co%2Fimage%2F"
    url_completer = "?format=json&vocalRemoval=false&market=from_token"

    # first play song then lyrics btn will be visible
    try:
        play_button = webdriver.find_element_by_xpath('/html/body/div[4]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div/div/div[2]/main/section/div[3]/div[4]/div/div/div/div/div/button').click()
        sleep(4)
    except:
        try:
            play_button = webdriver.find_element_by_xpath('/html/body/div[4]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div/div/div[2]/main/section/div[3]/div[4]/div/div/div/div/div/button').click()
            sleep(4)
        except:
            try:
                play_button = webdriver.find_element_by_xpath('/html/body/div[4]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div/div/div[2]/main/section/div[3]/div[4]/div/div/div/div/div/button').click()
                sleep(4)
            except:
                try:
                    play_button = webdriver.find_element_by_xpath('/html/body/div[4]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div/div/div[2]/main/section/div[3]/div[4]/div/div/div/div/div/button').click()
                    sleep(4)
                except:
                    play_button = webdriver.find_element_by_xpath('/html/body/div[4]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div/div/div[2]/main/section/div[3]/div[4]/div/div/div/div/div/button').click()
                    sleep(4)

    # first click on lyrics button before downloading lyrics
    try:
        lyrics_button = webdriver.find_element_by_xpath('/html/body/div[4]/div/div[2]/div[2]/footer/div/div[3]/div/button').click()
        sleep(8)
    except:
        lyrics_button = webdriver.find_element_by_xpath('/html/body/div[4]/div/div[2]/div[2]/footer/div/div[3]/div/button').click()
        sleep(8)


    # create lyrics url
    lyrics_url = f'https://spclient.wg.spotify.com/color-lyrics/v2/track/{track_id}/{middle_code}{track_key}{url_completer}'

    # open lyrics url   
    webdriver.get(lyrics_url)
    sleep(10)

    # get lyrics now
    try:
        lyrics = webdriver.find_element_by_xpath('/html/body/pre').text
    except:
        lyrics = webdriver.find_element_by_xpath('/html/body/pre').text

    # get it to json
    data = json.loads(lyrics)

    PATH_to_lyrics = PATH_for_json + "\\" + track_id + ".json"

    # save json to lyrics.json file
    with open(PATH_to_lyrics, 'w') as outfile:
        json.dump(data, outfile)
        
    sleep(4)

    return PATH_to_lyrics


def lyricsDownload(URL_of_track='https://open.spotify.com/track/6UelLqGlWMcVH1E5c4H7lY', PATH_for_json=""):
    sleep(2)
    try:
        login()
    except:
        login()
    
    try:
        path_to_lyrics = open_song_on_url(URL_of_track, PATH_for_json)
    except:
        try:
            path_to_lyrics = open_song_on_url(URL_of_track, PATH_for_json)
        except:
            try:
                path_to_lyrics = open_song_on_url(URL_of_track, PATH_for_json)
            except:
                path_to_lyrics = open_song_on_url(URL_of_track, PATH_for_json)
    logOut()
    return path_to_lyrics



if __name__ == '__main__':
    print("hello world")
#-----------
