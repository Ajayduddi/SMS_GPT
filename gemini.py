
import os
import google.generativeai as genai
from config import GEMINI_API_KEY
from gemini_data import SYSTEM_INSTRUCTION, CHAT_HISTORY

# Configure API
genai.configure(api_key=GEMINI_API_KEY)

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-2.0-flash",
  generation_config=generation_config,
  system_instruction=SYSTEM_INSTRUCTION,
)

# Start chat session
chat_session = model.start_chat(
  history=CHAT_HISTORY
)

def send_message(message):
  try:
    response = chat_session.send_message(message)
    return response.text
  except Exception as e:
    return f"Error sending message: {e}"

def send_audio(file_path):
  print('Sending audio:', file_path)
  try:
    # Open audio file
    with open(file_path, 'rb') as audio_file:
      audio_content = audio_file.read()
    
    # Start chat with the provided audio content formatted correctly
    response = chat_session.send_message({"parts": [{"mime_type": "audio/wav", "data": audio_content}]})
    return response.text

  except Exception as e:
    return f"Oops! 😅 There is an error with the bot: {str(e)}"
