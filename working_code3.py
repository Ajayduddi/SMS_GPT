import pyautogui
import pyperclip
import re
import time

def open_edge():
    #Open Microsoft Edge and navigate to Google Messages.
    #to avoid consequences fixing the web browser
    pyautogui.hotkey('win', '1')  # Open Edge (assuming it's pinned to taskbar position 1)
    time.sleep(2)
    
    pyautogui.hotkey('alt', 'd')  # Focus address bar
    pyautogui.write('https://messages.google.com/web/conversations')
    pyautogui.press('enter')
    
    time.sleep(8)  # Wait for page load

def copy_messages():
    """Copy all visible text from Messages before opening a chat."""
    time.sleep(2)
    
    pyautogui.hotkey('ctrl', 'a')  # Select all text
    pyautogui.hotkey('ctrl', 'c')  # Copy text
    time.sleep(1)
    
    return pyperclip.paste().strip()

def extract_latest_message(all_text):
    """Extract the latest message from the copied text using regex."""
    pattern = r"Conversation list(.*?)\n(.*?)\n(.*?)\n"
    match = re.search(pattern, all_text, re.DOTALL)
    
    if match:
        latest_message = match.group(3).strip()
        return latest_message if latest_message else None
    
    return None

def open_first_chat():
    """Open the first chat in the list."""
    time.sleep(2)
    
    pyautogui.press('tab', presses=3, interval=0.3)  # Navigate to first chat
    pyautogui.press('enter')
    
    time.sleep(5)  # Wait for chat to load

def searchChatGPT(query):
    """Search the latest message in ChatGPT and copy the response."""
    if not query:
        return None
    

    if query.endswith("--?"):
        query_with_instruction = f"{query} (in one paragraph only)"
    elif query.endswith("?"):
        query_with_instruction = query  # Send normally
    else:
        print("⚠️ Not a query, no response needed.") #for debugging purpose
        return None  # Not a query & do nothing

    # Open ChatGPT
    pyautogui.hotkey('ctrl', 't')  # Open new tab
    time.sleep(2)
    
    pyautogui.hotkey('alt', 'd')
    pyautogui.write('https://chat.openai.com')
    pyautogui.press('enter')
    
    time.sleep(10)  # Wait for chatgpt to load completely
    
    pyautogui.press('enter')  # Ensure input field is selected
    
    # Paste and send modified query
    pyperclip.copy(query_with_instruction)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')
    
    time.sleep(10)  # Wait for response generation
    
    # Use Shift+Tab 5 times to select response
    pyautogui.keyDown('shift')
    for _ in range(5):
        pyautogui.press('tab')
        time.sleep(0.3)
    pyautogui.keyUp('shift')
    
    pyautogui.press('enter')  # Copy response
    time.sleep(2)
    
    return pyperclip.paste().strip()

def sendResponseToSMS(response):
    """Send the copied ChatGPT response back as an SMS."""
    if not response:
        return
    
    # Switch back to Messages tab
    pyautogui.hotkey('ctrl', '1')
    time.sleep(3)
    
    # Paste and send response
    pyperclip.copy(response)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')

def main():
    """Main function to automate the process."""
    open_edge()
    
    # Copy messages before opening chat
    all_text = copy_messages()
    
    latest_message = extract_latest_message(all_text)
    
    open_first_chat()
    
    if latest_message:
        response = searchChatGPT(latest_message)
        sendResponseToSMS(response)

if __name__ == "__main__":
    main()
