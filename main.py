import pyautogui
import pyperclip
import re
import time
import requests
import logging
from langdetect import detect, LangDetectException
from deep_translator import GoogleTranslator
import pyaudio
import wave
import gemini
from config import *

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

pyautogui.FAILSAFE = True

class SMSBot:
    def __init__(self):
        self.loader = ""
        self.last_question = ""
        self.is_processing = False

    def open_edge(self):
        """Opens Edge browser and waits for it to load."""
        logger.info("Opening Edge...")
        pyautogui.hotkey('win', 'r')
        time.sleep(0.5)
        pyautogui.write('msedge')
        pyautogui.press('enter')
        time.sleep(0.5)
        
        self.wait_for_text_in_clipboard("loaded", action=lambda: pyautogui.write("loaded"))
        pyperclip.copy('cleartext')

    def open_messages(self):
        """Navigates to Google Messages web interface."""
        logger.info("Opening Google Messages...")
        time.sleep(0.5)
        pyautogui.hotkey('alt', 'd')
        pyautogui.write(GOOGLE_MESSAGES_URL)
        pyautogui.press('enter')

        self.wait_for_text_in_clipboard("Conversations")
        pyperclip.copy('cleartext')

    def wait_for_text_in_clipboard(self, target_text, action=None):
        """Waits until target_text appears in clipboard content."""
        self.loader = ""
        while target_text not in self.loader:
            time.sleep(0.5)
            if action:
                action()
            time.sleep(0.5)
            self.copy_all_to_clipboard()
            self.loader = pyperclip.paste()
        self.loader = ""

    def copy_all_to_clipboard(self):
        """Selects all text and copies to clipboard."""
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.5)

    def open_latest_chat(self):
        """Selects the latest chat from the conversation list."""
        time.sleep(2)
        for _ in range(4):
            pyautogui.press('tab')
            time.sleep(0.2)
        pyautogui.press('enter')
        time.sleep(1)

    def get_random_joke(self):
        try:
            response = requests.get(JOKE_API_URL)
            data = response.json()
            return f"{data['setup']} {data['punchline']}"
        except Exception as e:
            logger.error(f"Error fetching joke: {e}")
            return "Sorry, couldn't fetch a joke at the moment."

    def translate_text(self, text, target_lang):
        try:
            return GoogleTranslator(source="auto", target=target_lang).translate(text)
        except Exception as e:
            logger.error(f"Error translating text: {e}")
            return text

    def get_news(self, language, region):
        try:
            params = {
                "apiKey": NEWS_API_KEY,
                "language": language,
                "q": region,
                "pageSize": 1
            }
            response = requests.get(NEWS_API_URL, params=params)
            articles = response.json().get("articles", [])
            
            if not articles:
                return f"No news available for {region} right now."

            news_item = articles[0]
            return f"{news_item['title']} - {news_item['source']['name']}"
        except Exception as e:
            logger.error(f"Error fetching news: {e}")
            return f"Failed to fetch news for {region}."

    def detect_language(self, text):
        try:
            detected_lang = detect(text)
            return "en" if detected_lang == "nl" else detected_lang
        except LangDetectException:
            return "en"

    def send_response(self, response_text):
        """Types and sends the response in the message box."""
        # Navigate to input box (assuming specific tab sequence)
        # Check if we need to navigate or if we are already there?
        # The original code did random tabs/ups. Let's stick to its logic for safety
        # or just paste. The original 'gemini' function did tab/up loops.
        
        # Original gemini func logic:
        # for _ in range(3): pyautogui.press('tab')
        # for _ in range(3): pyautogui.press('up')
        # pyautogui.press('enter')
        # time.sleep(1)
        
        # NOTE: This navigation seems very specific to the user's screen resolution/state.
        # I will preserve it but put it in a method.
        self.focus_input_box()
        
        pyperclip.copy(response_text)
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('enter')

    def focus_input_box(self):
        """Attempts to focus the chat input box."""
        for _ in range(3):
            pyautogui.press('tab')
        for _ in range(3):
            pyautogui.press('up')
        pyautogui.press('enter')
        time.sleep(1)

    def chat_gpt_fallback(self, question, instruction):
        """Interacts with ChatGPT for fallback."""
        logger.info("Using ChatGPT fallback...")
        self.is_processing = True
        self.focus_input_box() # Just to follow previous logic pattern? Original did it at start of func.

        pyautogui.hotkey('ctrl', 't')
        time.sleep(0.5)
        pyautogui.hotkey('alt', 'd')
        pyautogui.write(CHATGPT_URL)
        pyautogui.press('enter')
        time.sleep(4)

        pyperclip.copy(f"{question} {instruction}")
        time.sleep(0.5)
        
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('enter')
        
        wait_time = 6 if question.endswith('--?') else 11
        time.sleep(wait_time)

        tabs = 6 if question.endswith('--?') else 7
        for _ in range(tabs):
            pyautogui.hotkey('shift', 'tab')
            time.sleep(0.2)
        
        pyautogui.press('enter')
        time.sleep(0.5)

        pyautogui.hotkey('ctrl', 'w') # Close tab
        time.sleep(0.5)
        pyautogui.hotkey('ctrl', 'v') # Paste result
        pyautogui.press('enter')

    def record_audio(self):
        """Records system audio."""
        logger.info("Recording audio...")
        audio = pyaudio.PyAudio()
        
        # device_index = AUDIO_DEVICE_INDEX # Use config value
        # But for safety, let's keep the hardcoded check or try to find it?
        # Original hardcoded 18.
        
        try:
            stream = audio.open(format=pyaudio.paInt16, channels=AUDIO_CHANNELS, rate=AUDIO_RATE,
                                input=True, input_device_index=AUDIO_DEVICE_INDEX,
                                frames_per_buffer=AUDIO_CHUNK_SIZE)
            
            frames = []
            
            # Navigate to play audio? Original Loop
            self.focus_input_box() # Is this right? Original code did 3 tabs, enter, 3 ups...
            # The original record_audio navigation was different.
            # Let's preserve the specific navigation for audio recording start.
             # Open top message
            for _ in range(3): pyautogui.press('tab')
            pyautogui.press('enter')
            for _ in range(3): pyautogui.press('up')
            time.sleep(1)
            for _ in range(31): pyautogui.press('tab') # ?!
            time.sleep(0.5)
            pyautogui.press('enter')

            print("Recording system audio...")
            for _ in range(600): # approx 10-15 seconds depending on chunk size/rate? 
                # Chunk 1024 / 48000 = 0.02s per chunk. 600 * 0.02 = 12 seconds.
                try:
                    data = stream.read(AUDIO_CHUNK_SIZE)
                    frames.append(data)
                except KeyboardInterrupt:
                    break
            
            stream.stop_stream()
            stream.close()
            audio.terminate()

            wf = wave.open(AUDIO_OUTPUT_FILENAME, 'wb')
            wf.setnchannels(AUDIO_CHANNELS)
            wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
            wf.setframerate(AUDIO_RATE)
            wf.writeframes(b''.join(frames))
            wf.close()

            response = gemini.send_audio("./" + AUDIO_OUTPUT_FILENAME)
            
            # Paste response
            pyperclip.copy(response)
            for _ in range(6): pyautogui.press('tab')
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.press('enter')

            # Delete audio message cleanup
            # This is very fragile but preserving original logic
            for _ in range(35): pyautogui.press('tab')
            pyautogui.press('enter')
            time.sleep(1)
            pyautogui.press('down')
            pyautogui.press('enter')
            time.sleep(1)
            pyautogui.press('tab')
            pyautogui.press('enter')
            time.sleep(0.5)

        except Exception as e:
            logger.error(f"Error in audio recording: {e}")

    def process_loop(self):
        """Main loop to check for messages."""
        logger.info("Starting processing loop...")
        while True:
            try:
                self.check_for_updates()
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                time.sleep(2) # Prevent rapid loop on error

    def check_for_updates(self):
        time.sleep(2.5)
        self.copy_all_to_clipboard()
        all_text = pyperclip.paste()
        
        # Regex to find the last message not from "You"
        pattern = r"Conversations list.*?\n.*?\n(?!You:)([^\n]*)"
        match = re.search(pattern, all_text)
        
        if match:
            new_question = match.group(1).strip()
            if new_question != self.last_question and new_question:
                logger.info(f"New Question Detected: {new_question}")
                self.last_question = new_question
                self.handle_question(new_question)
                self.is_processing = True

        if self.is_processing:
            self.open_messages()
            self.is_processing = False

    def handle_question(self, question):
        if "HELP 4 -" in question:
            self.handle_joke(question)
        elif "HELP 5 -" in question:
            self.handle_news(question)
        elif question.startswith('Audio clip'):
            self.record_audio()
        elif question.endswith('--?') or question.endswith('?'): # General query
            self.handle_ai_query(question)

    def handle_joke(self, question):
        match = re.search(r"HELP 4 -(.*)", question)
        if match:
            lang = match.group(1).strip()
            self.open_latest_chat()
            joke = self.get_random_joke()
            translated_joke = self.translate_text(joke, lang)
            self.send_response(translated_joke)

    def handle_news(self, question):
        match = re.search(r"HELP 5 -(\S+)\s*(.*)", question)
        if match:
            lang = match.group(1).strip()
            region = match.group(2).strip() if match.group(2) else "World"
            news = self.get_news(lang, region)
            self.open_latest_chat()
            
            pyperclip.copy(news)
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.press('enter')

    def handle_ai_query(self, question):
        detected_lang = self.detect_language(question)
        
        if question.startswith('/chatgpt'):
            instruction = f"Answer in {detected_lang}."
            if question.endswith('?'): # Detailed
                instruction += " Give a detailed answer within 1200 characters."
            else: # Short
                instruction += " Answer very shortly."
            self.chat_gpt_fallback(question, instruction)
        else:
            # Gemini default
            # Need to navigate to focus before sending? 
            # Origin logic called function 'gemini' which did navigation.
            self.focus_input_box()
            response = gemini.send_message(question)
            
            pyperclip.copy(response)
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.press('enter')

if __name__ == "__main__":
    bot = SMSBot()
    # Initial startup sequence
    bot.open_edge()
    bot.open_messages()
    bot.process_loop()
