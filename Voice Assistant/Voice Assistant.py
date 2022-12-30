import pyttsx3
import speech_recognition 
import datetime
import PyPDF2
import wikipedia
import webbrowser
import os
import smtplib
import time


#setting voices
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id) #Two voices are available  by default(David at index 0 & Zira at index 1)


#function for speaking
def speak(audio):
    engine.say(audio)
    engine.runAndWait()


#function for wishing
def Greet():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")
    elif hour>=12 and hour<18:
        speak("Good Afternoon!")
    elif hour>=18 and hour<20:
        speak("Good Evening!")
    else:
        speak("Good Night!")
    speak("I am Jarvis Sir. Please tell me how may I help you.")
    speak("Before that can you tell me your name?")
    global name
    name = takeCommand()
    speak(f"Hello{name}.Please tell me how can I help you.")
   


#function for taking command from user and returning it in form of string 
def takeCommand():
    # It takes in microphone input from the user and returns output in form of string.
    recognition = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        print("Listening...")
        recognition.pause_threshold = 1
        audio = recognition.listen(source)

    try:
        print("Recognizing...")
        query = recognition.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    
    except Exception:
        print(f"Say that again please {name}...")
        return "None"
    
    return query


#function for timer 
def timerMin(t):
    while(t):
        mins, secs = divmod(t, 60) 
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        t -=1
    speak(f"Time over {name}.")

#function for audiobook
def audio_book():
    speak("We have these books sir, select one to read.")
    print("A: Ikigai, B: Can't Hurt Me, C: Limitless")
    speak("A: ikigai, B: can't hurt me, C: limitless")

    choice = takeCommand()
    try:
        if choice == "a":
            speak("Reading Ikigai")
            book = open('sample_for_audiobook2.pdf', 'rb')
            pdfRead = PyPDF2.PdfReader(book)
            pages_n = len(pdfRead.pages)
            print(pages_n)
            speak(f"The number of pages is{pages_n}")
            for num in range(11,pages_n):
                page = pdfRead.pages[num]
                text = page.extract_text()
                speak(text)
        elif choice == "b":
            speak("Reading can't hurt me")
            book = open('sample_for_audiobook1.pdf', 'rb')
            pdfRead = PyPDF2.PdfReader(book)
            pages_n = len(pdfRead.pages)
            print(pages_n)
            speak(f"The number of pages is{pages_n}")
            for num in range(4,pages_n):
                page = pdfRead.pages[num]
                text = page.extract_text()
                speak(text)
        elif choice == "c":
            speak("Reading limitless")
            book = open('sample_for_audiobook3.pdf', 'rb')
            pdfRead = PyPDF2.PdfReader(book)
            pages_n = len(pdfRead.pages)
            print(pages_n)
            speak(f"The number of pages is{pages_n}")
            for num in range(22,pages_n):
                page = pdfRead.pages[num]
                text = page.extract_text()
                speak(text)
    except Exception:
        speak(f"Sorry {name}, not able to find this book currently. Try again")

#function for sending mail parameters required- to whom, content of mail 
def sendMail(to, content):
    #The port 587 is the port used by TLS, the encryption standard. May be different rarely.
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('emailHere@gmail.com', 'passwordHere')
    server.sendmail('akashchaute@gmail.com', to, content)
    server.close()




if __name__ == "__main__" :
    # Greet()
    while True:
        query = takeCommand().lower()
        #Execution of tasks based on query

        #for request on wikipedia
        if 'wikipedia' in query:
            speak(f'Searching Wikipedia, please wait {name}.')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences= 3)
            print(results)
            speak(results)

        #for request on timer
        elif 'countdown' in query:
            try:
                speak(f"Tell me the time in minutes please {name}.")
                t = takeCommand()
                t = int(t)
                t = t*60
                timerMin(t)
            except Exception:
                speak(f"Sorry my friend{name}. I am not able to start countdown at this moment please try again.")


        #for request on opening youtube
        elif 'open youtube' in query:
            speak(f"Please wait{name}, opening youtube.")
            webbrowser.open("youtube.com")
        #for request on opening stackoverflow
        elif 'open stackoverflow' in query:
            webbrowser.open("stackoverflow.com")


        #for request on opening music
        elif 'play music' in query:
            music_dir = 'E:\\Music'
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir,songs[0]))


        #for request on asking time
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            print(strTime)
            speak(f"{name}, the time is {strTime}")


        #for request on opening VScode
        elif 'open code' in query:
            codePath = "C:\\Users\\akash\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)


        #for request on sending email
        elif 'email to Akash' in query:
            try:                          #try isliye kyuki jarvis achanak band nhi hona chahiye
                speak("What Should I say?")
                content = takeCommand()
                to = "akashchaute@gmail.com"
                sendMail(to, content)
                speak("Email has been sent.")
            except Exception:
                speak(f"Sorry my friend{name} . I am not able to send this mail.")

        #request for reading audiobook
        elif 'audio book' or 'book' or 'read book' in query:
            audio_book()


        #for request of exit
        elif 'quit' or 'exit' in query:
            speak(f"Thank you, {name}.")
            exit()
