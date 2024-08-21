## Advanced Currency Converter with Tkinter GUI and Voice Input

### 🌍 **Project Overview**

This advanced currency converter application is built with Python's Tkinter library, featuring a sleek and futuristic GUI. It offers functionality for both live and offline currency conversions and incorporates interactive voice input for a modern user experience. 

### 🔧 **Features**

- **Currency Conversion**:
  - **Live Mode**: Fetches real-time exchange rates from online sources.
  - **Offline Mode**: Uses pre-defined exchange rates stored locally for conversion.
  - **Currency List**: Supports conversions between at least 10 currencies.

- **Voice Input Functionality**:
  - **Voice Commands**: Convert currencies using commands like "convert 100 USD to EUR".
  - **Microphone Control**: Start and stop listening for voice commands with a single click on the microphone icon.

- **User Interface**:
  - **Professional Design**: Features a modern, clean, and intuitive interface.
  - **Mode Toggle**: Easily switch between live and offline modes with a dedicated button.
  - **Microphone Integration**: Includes a microphone button for voice command input.

### 💻 **Technical Details**

- **Languages & Libraries**:
  - Python
  - Tkinter for GUI
  - Requests for API calls
  - Pygame for audio effects
  - SpeechRecognition for voice input
  - Threading for concurrent tasks

- **Code Highlights**:
  - **Tkinter Setup**: The main window is centered on the screen with a custom color scheme.
  - **Voice Recognition**: Integrated using the `speech_recognition` library, with support for recognizing and processing voice commands.
  - **Currency Data**: Exchange rates are fetched from an API in live mode and stored locally for offline use.
  - **Audio Effects**: Utilizes Pygame's mixer to play sound effects on currency conversion.

### 🚀 **How to Run**

1. **Install Dependencies**:
   - Make sure to install the required libraries using pip:
     ```bash
     pip install requests pygame SpeechRecognition
     ```

2. **Download Required Assets**:
   - Place the microphone image (`microphone.png`) and audio file (`music2.mp3`) in the specified directories.

3. **Run the Application**:
   - Execute the script:
     ```bash
     python currency_converter.py
     ```

4. **Configure API Key**:
   - Ensure you replace `"zapmf2lDkQ47hEsqjL57hNrYcHijnO6z"` with your own API key in the code for live currency conversion.

### 🛠 **Future Enhancements**

- **Expanded Currency Support**: Adding more currencies and improving offline rate accuracy.
- **Enhanced Voice Command Recognition**: Improving speech-to-text accuracy and command processing.
- **User Preferences**: Allow users to save their preferred settings and default currencies.

### 📂 **Repository**

Feel free to clone the repository, explore the code, and contribute! For any issues or feature requests, please open an issue on GitHub.
