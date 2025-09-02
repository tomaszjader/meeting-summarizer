# Meeting Summarizer 🎯

An automated meeting transcription and summarization system powered by OpenAI artificial intelligence.

## 📋 Description

Meeting Summarizer is a Python application that enables:
- **Real-time meeting recording**
- **Audio-to-text transcription** using OpenAI Whisper
- **Automatic meeting summarization** with key information extraction
- **Professional HTML notes generation**
- **Email distribution** of notes to meeting participants
- **Data storage** in JSON format

## ✨ Features

### 🎙️ Audio Recording
- Live recording from meetings
- Support for existing audio files
- Automatic splitting of large audio files

### 🤖 Artificial Intelligence
- Transcription using OpenAI Whisper
- Intelligent meeting summarization
- Key topics extraction
- Action items identification
- Decision recognition

### 📝 Documentation Generation
- Professional HTML notes
- JSON data export
- Clean format with thematic sections

### 📧 Communication
- Automatic email distribution of notes
- Configurable SMTP
- Multiple recipients support

## 🚀 Installation

### Requirements
- Python 3.7+
- OpenAI API key
- Microphone (for live recording)

### Installation Steps

1. **Clone or download the project**
```bash
git clone <repository-url>
cd meeting-summarizer
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables**

Create a `.env` file in the project root directory:
```env
# OpenAI API
OPENAI_API_KEY=your_openai_api_key_here

# Email Configuration (optional)
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USERNAME=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
```

### Getting OpenAI API Key
1. Register at [platform.openai.com](https://platform.openai.com)
2. Go to API Keys section
3. Create a new API key
4. Copy the key to your `.env` file

## 📖 Usage

### Running the Application
```bash
python mian.py
```

### Usage Options

**Option 1: Recording a new meeting**
- Select option "1" from the menu
- Specify recording duration or press Enter for manual stop
- The application will automatically record, transcribe, and summarize the meeting

**Option 2: Using an existing audio file**
- Select option "2" from the menu
- Provide the path to the audio file
- The application will process the file and create a summary

### Supported Audio Formats
- WAV
- MP3
- M4A
- FLAC
- Other formats supported by pydub

## 📁 Output File Structure

After processing a meeting, the application generates:

```
meeting_YYYYMMDD_HHMMSS.json    # Structured meeting data
notatki_YYYYMMDD_HHMMSS.html    # HTML formatted notes
meeting_audio.wav               # Audio file (if recorded)
```

### JSON Data Format
```json
{
  "summary": "Main meeting summary",
  "key_topics": ["Topic 1", "Topic 2"],
  "action_items": ["Task 1", "Task 2"],
  "decisions": ["Decision 1", "Decision 2"],
  "next_meeting": {},
  "participants": [],
  "transcript": "Full transcription..."
}
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key | ✅ |
| `EMAIL_SMTP_SERVER` | SMTP server | ❌ |
| `EMAIL_PORT` | SMTP port | ❌ |
| `EMAIL_USERNAME` | Email login | ❌ |
| `EMAIL_PASSWORD` | Email password | ❌ |

### Gmail Email Configuration
1. Enable two-factor authentication
2. Generate an app password
3. Use the app password in the `EMAIL_PASSWORD` variable

## 🛠️ Troubleshooting

### Audio Recording Issues
- **Windows**: Install Microsoft Visual C++ Build Tools
- **macOS**: `brew install portaudio`
- **Linux**: `sudo apt-get install portaudio19-dev`

### OpenAI API Issues
- Check API key validity
- Ensure sufficient funds in your OpenAI account
- Check API limits

### Email Issues
- Check SMTP configuration
- For Gmail, use app password, not account password
- Check email account security settings

## 📦 Dependencies

- `openai>=0.27.0` - OpenAI API for transcription and summarization
- `python-dotenv>=1.0.0` - .env file support
- `pyaudio>=0.2.11` - Audio recording
- `pydub>=0.25.1` - Audio file processing

## 🤝 Contributing

If you want to contribute to the project:
1. Fork the repository
2. Create a branch for your feature
3. Make your changes
4. Create a Pull Request

## 📄 License

This project is available under the MIT License. See the LICENSE file for details.

## 🆘 Support

If you encounter issues or have questions:
1. Check the "Troubleshooting" section
2. Create an issue in the repository
3. Contact the project author

---

**Meeting Summarizer** - Automating meeting documentation with AI 🚀