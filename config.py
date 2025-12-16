import os

# API Keys
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
NEWS_API_KEY = "bcd9b06b8b2f43cb9ac133f2b46fbc92"  # Recommend moving to env var

# APIs
JOKE_API_URL = "https://official-joke-api.appspot.com/jokes/random"
NEWS_API_URL = "https://newsapi.org/v2/top-headlines"

# Audio Settings
AUDIO_FORMAT_INT = 16  # pyaudio.paInt16 is int 8, but usually passed as constant. 
# We need to import pyaudio to use its constants if we want to be strict, 
# but for a config file, pure values or re-exporting might be cleaner. 
# For now, let's keep simple constants and handle the paInt16 conversion in main.
AUDIO_CHANNELS = 1
AUDIO_RATE = 48000
AUDIO_CHUNK_SIZE = 1024
AUDIO_OUTPUT_FILENAME = "output.wav"
AUDIO_DEVICE_INDEX = 18 # Hardware specific!

# Automation Settings
EDGE_HOTKEY = ('win', '7')
GOOGLE_MESSAGES_URL = 'https://messages.google.com/web/conversations'
CHATGPT_URL = 'https://chat.openai.com'
