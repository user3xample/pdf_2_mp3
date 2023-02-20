#! /usr/bin/env python3
"""
Program to take a PDF file and transcribe it into a spoken mp3 file
"""

import pyttsx3
import PyPDF2
import art
from os import system,name
from time import sleep

# Spoken Word default Settings
spoken_gender = 1  # 0 male , 1 female
spoken_speed = 160  # 160 is about right


def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def banner():
    sleep(1)
    clear()
    line = ("-" * 80)
    print(art.logo)
    print(f"{line}\n- PDF to spoken word MP3 converter\n{line}")


def voice_choice():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    voice_number = 1
    for voice in voices:
        print(f"Voice ID: {voice_number}")
        voice_number += 1
        print(f"Voice available: {voice.name}")
        engine.setProperty('voice', voice.id)
        engine.say('The quick brown fox jumped over the lazy dog.')
        engine.runAndWait()
        if voice_number == 3:
            break

    choice = int(input("What voice do you want to use? [voice ID] "))
    print(f"Setting the voice to use as : voice {choice}")
    return choice


def rate_of_speed():

    request = True
    while request:
        spoken_speed = int(input("Set words per min too [1-200]: "))
        if spoken_speed > 0 or spoken_speed < 200:
            print(f"Playing at speed {spoken_speed}")
            request = False

    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', spoken_speed)
    engine.say('The quick brown fox jumped over the lazy dog.')
    engine.runAndWait()
    choice = str(input("Is this speed ok? [y/n]")).lower()
    if choice == "n" or choice == "no":
        rate_of_speed()
    else:
        print(f"Setting our speed of spoke word to {spoken_speed} wpm")
        return spoken_speed


def my_program():
    continue_prog = True
    while continue_prog:
        line = ("-" * 80)
        banner()
        print("  - Warning: Please be mindful of copyright. Dont be a dick.\n")
        print(f"Voice type set to: {spoken_gender}")
        print(f"Voice speed set to: {spoken_speed} wpm\n")
        pdf_file_to_read = input("PDF file name: ")
        mp3_file_name = input("Name output MP3 file [I will add the '.mp3']: ")

        print(f"{line}\nProcessing This may take some time...\n{line}")

        pdfreader = PyPDF2.PdfReader(f"{pdf_file_to_read}")

        my_text_dump = []
        for page in pdfreader.pages:
            text = page.extract_text()
            clean_text = text.strip().replace("\n", " ")
            my_text_dump.append(clean_text)

        # Take our list and convert to a string
        my_text_dump_string = ""

        for item in my_text_dump:
            my_text_dump_string += item

        # set up our speaker
        speaker = pyttsx3.init()
        # voice type
        voices = speaker.getProperty('voices')
        speaker.setProperty('voice', voices[spoken_gender].id)
        # rate of speach
        speaker.setProperty('rate', spoken_speed)

        speaker = pyttsx3.init()
        # Convert the dump into mp3
        speaker.save_to_file(my_text_dump_string, f"{mp3_file_name}.mp3")
        speaker.runAndWait()
        speaker.stop()
        print(f"Finished Processing...\nYour file {mp3_file_name}.mp3 can now be found in the folder\n{line}")

        convert_again = input("Would you like to convert another file? [y/n] : ").lower()
        if convert_again == "y" or convert_again == "yes":
            my_program()
        else:
            back_to_menu = input("Would you like to go back to the menu or end the program ['menu'/ 'end' ]: ").lower()
            if back_to_menu == "menu":
                main_menu()
            else:
                print("Program Terminating")
                exit(0)


def main_menu():
    dont_carry_on = True
    while dont_carry_on:
        banner()
        print("What would you like to do?\n\n1.'Set Voice'\n2.'Set speed of voice'\n3.'create mp3'")
        choice = int(input("\n[1, 2, or 3] : "))
        if choice == 1:
            global spoken_gender
            spoken_gender = voice_choice()

        elif choice == 2:
            global spoken_speed
            spoken_speed = rate_of_speed()
        elif choice == 3:
            my_program()


main_menu()
