from webbrowser import Chrome
import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import smtplib
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv

chrome_path = "S:\Projects\Web Crawler\chromedriver_win32\chromedriver"

engine = pyttsx3.init("sapi5")

voices = engine.getProperty("voices")  # getting details of current voice

engine.setProperty("voice", voices[0].id)


def sendEmail(to, content):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login("dummyemail779@gmail.com", "Dummy@E99")
    server.sendmail("dummyemail779@gmail.com", to, content)
    server.close()


def speak(audio):
    engine.say(audio)
    # Without this command, speech will not be audible to us.
    engine.runAndWait()


def wishme():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning Shubham")

    elif hour <= 12 and hour < 18:
        speak("Good Afternoon Shubham!")

    else:
        speak("Good Evening Shubham !")
    speak("I am Jarvis Sir Please tell me How may I help You !!")


def takeCommand():
    # It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.9
        audio = r.listen(source)

    try:
        print("Recognizing...")
        # Using google for voice recognition.
        query = r.recognize_google(audio, language="en-in")
        print(f"User said: {query}\n")  # User query will be printed.

    except Exception as e:
        # print(e)
        # Say that again will be printed in case of improper voice
        print("Say that again please...")
        return "None"  # None string will be returned
    return query


if __name__ == "__main__":
    wishme()
    while True:
        # if 1:
        query = takeCommand().lower()  # Converting user query into lower case

        # Logic for executing tasks based on query
        if (
            "wikipedia" in query
        ):  # if wikipedia found in the query then this block will be executed
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif "whatsapp" in query:
            speak("Opening Whatsapp for you...")
            print("Opening Whatsapp for you...")
            driver = webdriver.Chrome(chrome_path)
            driver.get("https://web.whatsapp.com/")
            driver.maximize_window()

            name = input("Enter name or group name:")
            msg = input("Enter message:")
            count = int(input("Enter count:"))

            input("Please press Enter after scanning  QR code")

            user = driver.find_element_by_xpath("//span[@title='{}']".format(name))
            user.click()

            msg_box = driver.find_element_by_xpath(
                "//*[@id='main']/footer/div[1]/div[2]/div/div[2]"
            )

            for index in range(count):
                msg_box.send_keys(msg)
                driver.find_element_by_xpath(
                    "//*[@id='main']/footer/div[1]/div[3]/button"
                ).click()

            print("Success")

        elif "open youtube" in query:
            speak("Opening Youtube...")
            driver = webdriver.Chrome(chrome_path)
            driver.get("http://www.youtube.com")

        # elif 'open google' in query:
        #     webbrowser.get(chrome_path).open("google.com")

        elif "open stack overflow" in query:
            speak("Opening Stack Over flow...")
            driver = webdriver.Chrome(chrome_path)
            driver.get("https://stackoverflow.com")

        elif "the time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")

        elif "play music" in query:
            music_dir = "S:\\Songs"
            speak("Playing music... Sir")
            songs = os.listdir(music_dir)
            os.startfile(os.path.join(music_dir, songs[0]))

        elif "play video" in query:
            vid_dir = "S:\\sagar"
            songs = os.listdir(vid_dir)
            os.startfile(os.path.join(vid_dir, songs[0]))

        elif "open google and search" in query:
            reg_ex = re.search("open google and search (.*)", query)
            search_for = query.split("search", 1)[1]
            url = "https://www.google.com/"
            if reg_ex:
                subgoogle = reg_ex.group(1)
                url = url + "r/" + subgoogle
            speak("Okay!")
            driver = webdriver.Chrome(chrome_path)
            driver.get("http://www.google.com")
            # search = driver.find_element_by_name('q')  # finds search
            search = driver.find_element_by_xpath(
                '//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input'
            )
            search.send_keys(str(search_for))
            search.send_keys(Keys.RETURN)

        elif "point" in query:
            speak("Switching to the Data Science section....")
            print("Data Science Mode On...")
            speak("Sir Please give the file location....")
            linech = input("Loacation:")
            with open(linech, "r") as f:
                reader = csv.reader(f)
                i = next(reader)
                print(i[0])

            df = pd.read_csv(linech)
            names = df[i[0]].values
            bar2 = df[i[1]].values
            plt.scatter(names, bar2, color="red", marker="o")
            plt.title(i[0] + " VS " + i[1], fontsize=14)
            plt.xlabel(i[0], fontsize=14)
            plt.ylabel(i[1], fontsize=14)
            plt.grid(True)
            plt.show()

        elif "line chart" in query:
            speak("Switching to the Data Science section....")
            print("Data Science Mode On...")
            speak("Sir Please give the file location....")
            linech = input("Loacation :")
            with open(linech, "r") as f:
                reader = csv.reader(f)
                i = next(reader)
                print(i[0])

            df = pd.read_csv(linech)
            names = df[i[0]].values
            bar2 = df[i[1]].values
            plt.plot(names, bar2, color="red", marker="o")
            plt.title(i[0] + " VS " + i[1], fontsize=14)
            plt.xlabel(i[0], fontsize=14)
            plt.ylabel(i[1], fontsize=14)
            plt.grid(True)
            plt.show()

        elif "send email to" in query:
            try:
                speak("Sir please Enter the Email address:")
                print("Please Enter Email Address:")
                to = input()
                speak("What should I say?")
                content = takeCommand()
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry my friend. I am not able to send this email")

        elif "data frame" in query:

            speak("Switching to the Data Science section....")
            speak("Sir Please give the file location....")
            ab = input("Location :")
            df = pd.read_csv(ab)
            kf = pd.DataFrame(df)
            # print(kf)

            speak("Sir what did you want to do with the Data frame ....")
            # express = takeCommand().lower()
            while True:
                try:
                    express = takeCommand().lower()
                    if "clean" in express:
                        speak("Sir Cleaning the data by Fill N A method .....")
                        # speak("what kind of")
                        kf2 = kf.fillna(kf.max())
                        print(kf2)

                    elif "find minimum of each" in express:
                        speak(
                            "Sir Minimum Value of Each column in the Given Data is...."
                        )
                        print("Minimum Value of Each column in the Given Data is:")
                        print(kf.min())

                    elif "find maximum of each" in express:
                        speak(
                            "Sir maximum Value of Each column in the Given Data is...."
                        )
                        print("maximum Value of Each column in the Given Data is:")
                        print(kf.max())

                    elif "find average of each" in express:
                        speak(
                            "Sir average Value of Each column in the Given Data is...."
                        )
                        print("average Value of Each column in the Given Data is:")
                        print(kf.max())

                    elif "find minimum" in express:
                        speak("Sir Minimum Value in the Given Data is....")
                        kfMin = kf.min()
                        print("Minimum Value in the Given Data is:")
                        print(kfMin.min())

                    elif "find maximum" in express:
                        speak("Sir Maximum Value in the Given Data is....")
                        kfMin = kf.max()
                        print("Maximum Value in the Given Data is:")
                        print(kfMin.max())

                    elif "find average" in express:
                        speak("Sir Average Value of the Given Data is....")
                        kfMin = kf.mean()
                        print("Average Value of the Given Data is:")
                        print(kfMin.mean())

                    elif "stop" in express:
                        speak("Good to see you sir...")
                        speak("Switching to the Normal Mode...")
                        print("Normal Mode On:")
                        break
                    continue
                except Exception as e:
                    speak("speak again sir...")
                    break

        # elif 'show location of' in query:
        #     location = re.search('show location of (.*)', query)
        #     search_for_location = query.split("of", 1)[1]
        #     url_location = 'https://google.nl/maps/place/'
        #     if location:
        #         subgoogle = location.group(1)
        #         url_location = url_location + 'r/' + subgoogle+'/&amp;'
        #     speak('Okay!')

        #     driver = webdriver.Chrome(chrome_path)
        #     driver.get(url_location)
        # search = driver.find_element_by_name('q')  # finds search
        # search = driver.find_element_by_xpath(
        #     '//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input')
        # search.send_keys(str(search_for))
        # search.send_keys(Keys.RETURN)
        elif "shutdown" in query:
            speak("Have a Good day Sir.........")
            exit()
