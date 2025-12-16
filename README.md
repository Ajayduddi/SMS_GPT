# SMS_GPT 🤖📱

**SMS_GPT** is an intelligent SMS chatbot that bridges **Google Messages (Web)** with **Google Gemini AI**. It automates your browser to read incoming SMS messages and replies using advanced AI models, effectively turning your phone number into a smart AI assistant.

> **Note**: This project uses desktop automation (`pyautogui`) to interact with the Google Messages web interface. It requires an active browser window.

## 🚀 Features

- **AI-Powered Conversations**: Chat naturally with Google's Gemini AI (default: `gemini-2.0-flash-exp`).
- **Device-Aware Responses**:
  - **Smartphones**: Rich responses with emojis and formatting.
  - **Feature Phones**: Concise, text-only responses (< 25 words).
- **Multi-Model Support**: Switch between generic AI response types using `/chatgpt` (simulated fallback) or native Gemini.
- **Smart Tools**:
  - **Jokes**: Ask for a joke! (e.g., "HELP 4 - en")
  - **News**: Get latest headlines. (e.g., "HELP 5 - en US")
  - **Audio Messages**: Can record and send audio replies (requires loopback device).
  - **Translation**: Auto-detects and responds in the user's language.
- **Location Awareness**: Handles "near me" queries by asking for location context.

## 🛠️ Architecture

- **`main.py`**: The automation engine. Uses `pyautogui` to screen-scrape Google Messages and type responses.
- **`gemini.py`**: Handles AI logic, connecting to Google's Generative AI API.
- **`gemini_data.py`**: Stores extensive system prompts and conversation history for persona management.
- **`config.py`**: Central configuration for API keys and settings.

## 📋 Prerequisites

- **OS**: Windows (preferred for audio/automation drivers).
- **Python**: 3.8 or higher.
- **Browser**: Microsoft Edge (configured in automation script).
- **Android Phone**: Linked to [Google Messages for Web](https://messages.google.com/web/).

## 📦 Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/yourusername/SMS_GPT.git
    cd SMS_GPT
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set Up Configuration**
    - The project expects a `GEMINI_API_KEY` environment variable.
    - Set it in your terminal or system settings:
      ```powershell
      $env:GEMINI_API_KEY="your_google_ai_api_key"
      ```
    - Alternatively, modify `config.py` to hardcode it (not recommended).

## 🏃 Usage

1.  **Prepare the Environment**
    - Open **Microsoft Edge**.
    - Log in to [Google Messages Web](https://messages.google.com/web/) and ensure your phone is paired.
    - Keep the browser window open.

2.  **Run the Bot**
    ```bash
    python main.py
    ```
    - The script will automatically try to focus the Edge window and navigate to the messages tab.
    - **Hand's Off!** Since this uses mouse/keyboard automation, avoid using the computer while it's running.

3.  **Interact via SMS**
    - Send an SMS to your phone number to test!
    - **"Hi"**: Triggers the welcome message.
    - **"What is AI??"**: Detailed smartphone response.
    - **"What is AI?--?"**: Short feature-phone response.

## ⚠️ Important Notes

- **Screen Resolution**: `pyautogui` relies on screen coordinates. If the script misses clicks, you may need to adjust the tab/navigation logic in `main.py`.
- **Audio Loopback**: Recording system audio requires a specific "Stereo Mix" or loopback driver enabled in Windows Sound settings. Update `AUDIO_DEVICE_INDEX` in `config.py` if needed.

## 🤝 Contributing

Feel free to submit issues or pull requests to improve the automation stability or add new AI features!
