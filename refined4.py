import pyautogui
import pyperclip
import re
import time
import requests
from langdetect import detect, LangDetectException
from deep_translator import GoogleTranslator
from gemini import send_audio, send_message
import pyaudio
import wave

# Global Variables
Loader = ''
Question = ''
flag = 0
FORMATE = pyaudio.paInt16
CHANNEL = 1
RATE = 44100
CHUNK = 1024
OUTPUT_FILENAME = "output.wav"

pyautogui.FAILSAFE = True  

# APIs
JOKE_API = "https://official-joke-api.appspot.com/jokes/random"
NEWS_API = "https://newsapi.org/v2/top-headlines"
NEWS_API_KEY = "bcd9b06b8b2f43cb9ac133f2b46fbc92"  # Replace with your actual API key

# Function to open Edge browser
def openEdge():
    global Loader
    pyautogui.hotkey('win', '7')  
    time.sleep(0.5)
    
    while "loaded" not in Loader:
        time.sleep(0.5)
        pyautogui.write("loaded")
        time.sleep(0.5)
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.5)
        Loader = pyperclip.paste()
    
    Loader = ''
    pyperclip.copy('cleartext')

# Function to open Google Messages
def openMessages():
    global Loader
    time.sleep(0.5)
    pyautogui.hotkey('alt', 'd')
    pyautogui.write('https://messages.google.com/web/conversations')
    pyautogui.press('enter')

    while "Conversations" not in Loader:
        time.sleep(0.5)
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.5)
        Loader = pyperclip.paste()
    
    Loader = ''
    pyperclip.copy('cleartext')

# Function to open the latest chat
def open_latest_chat():
    time.sleep(1)
    for _ in range(3):
        pyautogui.press('tab')
        time.sleep(0.2)
    pyautogui.press('enter')
    time.sleep(1)

# Function to fetch a joke
def get_random_joke():
    try:
        response = requests.get(JOKE_API)
        data = response.json()
        return f"{data['setup']} {data['punchline']}"
    except:
        return "Sorry, couldn't fetch a joke at the moment."

# Function to translate text
def translate_text(text, target_lang):
    try:
        return GoogleTranslator(source="auto", target=target_lang).translate(text)
    except:
        return text  

# Function to fetch news dynamically based on region
def get_news(language, region):
    try:
        params = {
            "apiKey": NEWS_API_KEY,
            "language": language,
            "q": region,
            "pageSize": 1
        }
        response = requests.get(NEWS_API, params=params)
        articles = response.json().get("articles", [])
        
        if not articles:
            return f"No news available for {region} right now."

        news_item = articles[0]  
        return f"{news_item['title']} - {news_item['source']['name']}"

    except:
        return f"Failed to fetch news for {region}."

# Function to detect language and treat Dutch as English
def detect_language(text):
    try:
        detected_lang = detect(text)
        if detected_lang == "nl":  # If the detected language is Dutch (nl), treat it as English (en)
            return "en"
        return detected_lang
    except LangDetectException:
        return "en"  # Fallback to English if the detection fails

# Function to process the latest message
def get_question():
    global Question, flag
    time.sleep(2.5)

    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.5)
    alltext = pyperclip.paste()

    # print("Clipboard content:", alltext)  # Debugging: print clipboard content
    
    pattern = r"Conversations list.*?\n.*?\n(?!You:)([^\n]*)"
    # pattern = r"Conversations list(.*?)\n(.*?)\n(.*?)\n"
    match = re.search(pattern, alltext)
    print("Match:", match)
    
    if match:
        Question = match.group(1).strip()
        print(f"Extracted Question: {Question}")  # Debugging: print extracted question
        
        if "HELP 4 -" in Question:  # If query is for joke
            lang_match = re.search(r"HELP 4 -(.*)", Question)
            if lang_match:
                open_latest_chat()
                time.sleep(1)
                lang = lang_match.group(1).strip()
                joke = get_random_joke()
                translated_joke = translate_text(joke, lang)
                
                pyperclip.copy(translated_joke)
                pyautogui.hotkey('ctrl', 'v')
                pyautogui.press('enter')
                
            flag = 1  # Ensures the script continues checking for new messages
        
        elif "HELP 5 -" in Question:  # If query is for news
            news_match = re.search(r"HELP 5 -(\S+)\s*(.*)", Question)
            if news_match:
                lang = news_match.group(1).strip()
                region = news_match.group(2).strip() if news_match.group(2) else "World"
                news = get_news(lang, region)
                
                open_latest_chat()
                time.sleep(1)
                pyperclip.copy(news)
                pyautogui.hotkey('ctrl', 'v')
                pyautogui.press('enter')

            flag = 1  # Ensures the script continues checking for new messages
        
        if Question.endswith('--?'):
            detected_lang = detect_language(Question)
            instruction = f"Answer very very shortly in {detected_lang}."
            
            if Question.startswith('/chatgpt'): 
                chatGPT(Question, instruction)
            else:
                gemini(Question)


        elif Question.endswith('') or Question.endswith('?'):
            detected_lang = detect_language(Question)
            instruction = f"Give a detailed answer in {detected_lang}. with in 1200 characters"
            
            if Question.startswith('/chatgpt'): 
                chatGPT(Question, instruction)
            else:
                gemini(Question)


# Function to handle ChatGPT responses
def gemini(question) :
    global flag
    flag = 1
    
    for _ in range(3):
        pyautogui.press('tab')
    for _ in range(3):
        pyautogui.press('up')
    pyautogui.press('enter')
    time.sleep(1)
    
    response = send_message( Question)
    pyperclip.copy(response)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')
    return

# Function to handle ChatGPT responses
def chatGPT(question, instruction):
    global flag
    flag = 1

    for _ in range(3):
        pyautogui.press('tab')
    for _ in range(3):
        pyautogui.press('up')
    pyautogui.press('enter')
    time.sleep(1)

    pyautogui.hotkey('ctrl', 't')
    time.sleep(0.5)
    pyautogui.hotkey('alt', 'd')
    pyautogui.write('https://chat.openai.com')
    pyautogui.press('enter')
    time.sleep(4)

    pyperclip.copy(f"{question} {instruction}")  
    time.sleep(0.5)
    
    if question.endswith('--?'):
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('enter')
        time.sleep(6)

        for _ in range(6):
            pyautogui.hotkey('shift', 'tab')
            time.sleep(0.2)
        pyautogui.press('enter')
        time.sleep(0.5)
    else :
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('enter')
        time.sleep(11)

        for _ in range(7):
            pyautogui.hotkey('shift', 'tab')
            time.sleep(0.2)
        pyautogui.press('enter')
        time.sleep(0.5)
 

    pyautogui.hotkey('ctrl', 'w')
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')


# Audio recording
def record_audio():
    audio  = pyaudio.PyAudio()
    stream = audio.open(format=FORMATE, channels=CHANNEL, rate=RATE, input=True, frames_per_buffer=CHUNK)
    frames = []

    for _ in range(28):
        pyautogui.press('tab')
    pyautogui.press('enter')
    time.sleep(1)
    print("Recording...")
    i = 500
    while i>0:
        try:
            data = stream.read(CHUNK)
            frames.append(data)
            i-=1
        except KeyboardInterrupt:
            break
    
    print("Done recording.")
    stream.stop_stream()
    stream.close()
    audio.terminate()

    wf = wave.open(OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNEL)
    wf.setsampwidth(audio.get_sample_size(FORMATE))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    
    name = "./output.wav"
    response = send_audio(name)
    print(response)
    pyperclip.copy(response)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')
    return

# Open required applications and start processing messages
# openEdge()
# openMessages()

record_audio()

# while True:
#     get_question()
#     if flag == 1:
#         openMessages()
#         flag = 0
