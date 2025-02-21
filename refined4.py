import pyautogui
import pyperclip
import re
import time
import requests
from langdetect import detect, LangDetectException
from deep_translator import GoogleTranslator

# Global Variables
Loader = ''
Question = ''
flag = 0

pyautogui.FAILSAFE = True  

# APIs
JOKE_API = "https://official-joke-api.appspot.com/jokes/random"
NEWS_API = "https://newsapi.org/v2/top-headlines"
NEWS_API_KEY = "bcd9b06b8b2f43cb9ac133f2b46fbc92"  # Replace with your actual API key

# Function to open Edge browser
def openEdge():
    global Loader
    pyautogui.hotkey('win', '2')  
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

    while "Conversation" not in Loader:
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

    print("Clipboard content:", alltext)  # Debugging: print clipboard content
    
    pattern = r"Conversation list(.*?)\n(.*?)\n(.*?)\n"
    match = re.search(pattern, alltext, re.DOTALL)
    
    if match:
        Question = match.group(3).strip()
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
             instruction = f"Give a detailed answer in {detected_lang}."
             chatGPT(Question, instruction)
        elif Question.endswith('?'):
             detected_lang = detect_language(Question)
             instruction = f"Answer very very shortly in {detected_lang}."
             chatGPT(Question, instruction)


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
    time.sleep(5)

    pyperclip.copy(f"{question} {instruction}")  
    time.sleep(0.5)
    
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')
    time.sleep(10)

    for _ in range(6):
        pyautogui.hotkey('shift', 'tab')
        time.sleep(0.2)
    pyautogui.press('enter')
    time.sleep(0.5)
    #pyautogui.hotkey('ctrl', 'c')

    pyautogui.hotkey('ctrl', 'w')
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')

# Open required applications and start processing messages
openEdge()
openMessages()

while True:
    get_question()
    if flag == 1:
        openMessages()
        flag = 0
