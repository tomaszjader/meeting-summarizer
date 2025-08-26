import openai
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import os
from typing import List, Dict
import re
import pyaudio
import wave
from dotenv import load_dotenv

# Załaduj zmienne środowiskowe z pliku .env
load_dotenv()

class MeetingSummarizer:
    def __init__(self, openai_api_key: str = None, email_config: Dict = None):
        """
        Inicjalizacja systemu Meeting Summarizer
        
        Args:
            openai_api_key: Klucz API dla OpenAI (opcjonalnie, można użyć z .env)
            email_config: Konfiguracja email (opcjonalnie, można użyć z .env)
        """
        # Inicjalizuj klienta OpenAI z nowym API
        api_key = openai_api_key or os.getenv('OPENAI_API_KEY')
        self.openai_client = openai.OpenAI(api_key=api_key)
        
        # Konfiguracja email z parametru lub z .env
        if email_config:
            self.email_config = email_config
        else:
            self.email_config = {
                'smtp_server': os.getenv('EMAIL_SMTP_SERVER', 'smtp.gmail.com'),
                'port': int(os.getenv('EMAIL_PORT', '587')),
                'username': os.getenv('EMAIL_USERNAME'),
                'password': os.getenv('EMAIL_PASSWORD')
            } if os.getenv('EMAIL_USERNAME') else {}
        
    def record_audio(self, filename: str = "meeting_audio.wav", duration: int = None):
        """
        Nagrywanie audio ze spotkania
        
        Args:
            filename: Nazwa pliku do zapisu
            duration: Czas nagrywania w sekundach (None = nagrywanie do przerwania)
        """
        print("🎤 Rozpoczynam nagrywanie spotkania...")
        
        # Konfiguracja nagrywania
        chunk = 1024
        format = pyaudio.paInt16
        channels = 1
        rate = 44100
        
        audio = pyaudio.PyAudio()
        
        stream = audio.open(
            format=format,
            channels=channels,
            rate=rate,
            input=True,
            frames_per_buffer=chunk
        )
        
        frames = []
        
        try:
            if duration:
                for _ in range(0, int(rate / chunk * duration)):
                    data = stream.read(chunk)
                    frames.append(data)
            else:
                print("Naciśnij Ctrl+C aby zakończyć nagrywanie...")
                while True:
                    data = stream.read(chunk)
                    frames.append(data)
                    
        except KeyboardInterrupt:
            print("\n🛑 Zatrzymano nagrywanie")
        
        stream.stop_stream()
        stream.close()
        audio.terminate()
        
        # Zapisz plik
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(audio.get_sample_size(format))
            wf.setframerate(rate)
            wf.writeframes(b''.join(frames))
        
        print(f"✅ Nagranie zapisane jako: {filename}")
        return filename



    def transcribe_audio(self, audio_file: str) -> str:
        """
        Transkrypcja używając OpenAI Whisper
        
        Args:
            audio_file: Ścieżka do pliku audio
            
        Returns:
            Transkrypcja spotkania
        """
        print("🤖 Transkrypcja przez OpenAI Whisper...")
        
        try:
            with open(audio_file, "rb") as audio:
                transcript = self.openai_client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio,
                    language="pl"
                )
            print("✅ Transkrypcja ukończona")
            return transcript.text
        except Exception as e:
            print(f"❌ Błąd transkrypcji OpenAI: {e}")
            return ""

    def summarize_meeting(self, transcript: str) -> Dict:
        """
        Podsumowanie spotkania używając GPT
        
        Args:
            transcript: Transkrypcja spotkania
            
        Returns:
            Dict z podsumowaniem, action items itp.
        """
        print("📋 Tworzę podsumowanie spotkania...")
        
        prompt = f"""
        Przeanalizuj poniższą transkrypcję spotkania i utwórz strukturalne podsumowanie:

        TRANSKRYPCJA:
        {transcript}

        Proszę o utworzenie podsumowania w formacie JSON zawierającego:
        1. "summary" - główne podsumowanie spotkania (2-3 akapity)
        2. "key_topics" - lista głównych tematów omawianych na spotkaniu
        3. "action_items" - lista konkretnych zadań do wykonania z odpowiedzialnymi osobami
        4. "decisions" - podjęte decyzje
        5. "next_meeting" - informacje o następnym spotkaniu (jeśli wspomniano)
        6. "participants" - lista uczestników (jeśli można wyciągnąć z transkrypcji)

        Odpowiedz tylko w formacie JSON, bez dodatkowego tekstu.
        """

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            # Parsuj JSON z odpowiedzi
            summary_json = json.loads(response.choices[0].message.content)
            print("✅ Podsumowanie utworzone")
            return summary_json
            
        except Exception as e:
            print(f"❌ Błąd tworzenia podsumowania: {e}")
            return {
                "summary": "Nie udało się utworzyć podsumowania",
                "key_topics": [],
                "action_items": [],
                "decisions": [],
                "next_meeting": "",
                "participants": []
            }

    def create_meeting_notes(self, meeting_data: Dict, meeting_title: str = None) -> str:
        """
        Tworzenie sformatowanych notatek ze spotkania
        
        Args:
            meeting_data: Dane podsumowania ze spotkania
            meeting_title: Tytuł spotkania
            
        Returns:
            Sformatowane notatki HTML
        """
        if not meeting_title:
            meeting_title = f"Spotkanie z dnia {datetime.now().strftime('%d.%m.%Y')}"
        
        html_notes = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>{meeting_title}</title>
            <style>
                body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
                h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; }}
                h2 {{ color: #34495e; margin-top: 30px; }}
                .action-item {{ background: #fff3cd; padding: 10px; margin: 5px 0; border-left: 4px solid #ffc107; }}
                .decision {{ background: #d4edda; padding: 10px; margin: 5px 0; border-left: 4px solid #28a745; }}
                ul {{ padding-left: 20px; }}
                .date {{ color: #6c757d; font-size: 0.9em; }}
            </style>
        </head>
        <body>
            <h1>{meeting_title}</h1>
            <p class="date">Data: {datetime.now().strftime('%d.%m.%Y, %H:%M')}</p>
            
            <h2>📋 Podsumowanie</h2>
            <p>{meeting_data.get('summary', 'Brak podsumowania')}</p>
            
            <h2>🎯 Główne tematy</h2>
            <ul>
                {"".join([f"<li>{topic}</li>" for topic in meeting_data.get('key_topics', [])])}
            </ul>
            
            <h2>✅ Zadania do wykonania (Action Items)</h2>
            {"".join([f'<div class="action-item"><strong>📌 {item}</strong></div>' for item in meeting_data.get('action_items', [])])}
            
            <h2>🎯 Podjęte decyzje</h2>
            {"".join([f'<div class="decision"><strong>✓ {decision}</strong></div>' for decision in meeting_data.get('decisions', [])])}
            
            <h2>👥 Uczestnicy</h2>
            <ul>
                {"".join([f"<li>{participant}</li>" for participant in meeting_data.get('participants', [])])}
            </ul>
            
            <h2>📅 Następne spotkanie</h2>
            <p>{meeting_data.get('next_meeting', 'Nie ustalono')}</p>
            
            <hr>
            <p><small>Notatki wygenerowane automatycznie przez Meeting Summarizer</small></p>
        </body>
        </html>
        """
        
        return html_notes

    def send_email_notes(self, notes_html: str, participants_emails: List[str], 
                        subject: str = None, sender_name: str = "Meeting Summarizer"):
        """
        Wysyłanie notatek uczestnikom przez email
        
        Args:
            notes_html: Notatki w formacie HTML
            participants_emails: Lista emaili uczestników
            subject: Temat emaila
            sender_name: Nazwa nadawcy
        """
        if not self.email_config:
            print("❌ Brak konfiguracji email")
            return
        
        if not subject:
            subject = f"Notatki ze spotkania - {datetime.now().strftime('%d.%m.%Y')}"
        
        print(f"📧 Wysyłam notatki do {len(participants_emails)} uczestników...")
        
        try:
            # Konfiguracja serwera SMTP
            server = smtplib.SMTP(self.email_config['smtp_server'], self.email_config['port'])
            server.starttls()
            server.login(self.email_config['username'], self.email_config['password'])
            
            for email in participants_emails:
                # Tworzenie wiadomości
                msg = MIMEMultipart('alternative')
                msg['Subject'] = subject
                msg['From'] = f"{sender_name} <{self.email_config['username']}>"
                msg['To'] = email
                
                # Dodaj treść HTML
                html_part = MIMEText(notes_html, 'html', 'utf-8')
                msg.attach(html_part)
                
                # Wyślij email
                server.send_message(msg)
                print(f"✅ Wysłano do: {email}")
            
            server.quit()
            print("✅ Wszystkie notatki wysłane")
            
        except Exception as e:
            print(f"❌ Błąd wysyłania email: {e}")

    def save_meeting_data(self, meeting_data: Dict, filename: str = None):
        """Zapisz dane spotkania do pliku JSON"""
        if not filename:
            filename = f"meeting_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(meeting_data, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Dane spotkania zapisane: {filename}")
        return filename

# Przykład użycia
def main():
    # Inicjalizacja - klucze będą pobrane z pliku .env
    summarizer = MeetingSummarizer()
    
    print("🎯 Meeting Summarizer - System transkrypcji i podsumowania spotkań")
    print("=" * 60)
    
    # Opcja 1: Nagrywanie na żywo
    choice = input("Wybierz opcję:\n1. Nagraj nowe spotkanie\n2. Użyj istniejący plik audio\nWybór (1/2): ")
    
    if choice == "1":
        # Nagrywanie spotkania
        duration = input("Podaj czas nagrywania w sekundach (Enter = ręczne zatrzymanie): ")
        duration = int(duration) if duration.isdigit() else None
        
        audio_file = summarizer.record_audio(duration=duration)
    else:
        # Użyj istniejący plik
        audio_file = input("Podaj ścieżkę do pliku audio: ")
    
    # Transkrypcja
    transcript = summarizer.transcribe_audio(audio_file)
    
    if not transcript:
        print("❌ Nie udało się utworzyć transkrypcji")
        return
    
    # Podsumowanie
    meeting_data = summarizer.summarize_meeting(transcript)
    meeting_data['transcript'] = transcript  # Dodaj transkrypcję do danych
    
    # Zapisz dane
    json_file = summarizer.save_meeting_data(meeting_data)
    
    # Utwórz notatki HTML
    meeting_title = input("Podaj tytuł spotkania (Enter = automatyczny): ") or None
    notes_html = summarizer.create_meeting_notes(meeting_data, meeting_title)
    
    # Zapisz notatki HTML
    html_filename = f"notatki_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    with open(html_filename, 'w', encoding='utf-8') as f:
        f.write(notes_html)
    print(f"📝 Notatki HTML zapisane: {html_filename}")
    
    # Wysyłanie emaili (opcjonalnie)
    send_emails = input("Czy chcesz wysłać notatki emailem? (t/n): ").lower() == 't'
    
    if send_emails and summarizer.email_config:
        emails_input = input("Podaj emaile uczestników (oddziel przecinkami): ")
        participant_emails = [email.strip() for email in emails_input.split(',')]
        
        summarizer.send_email_notes(notes_html, participant_emails)
    
    print("\n🎉 Meeting Summarizer zakończony!")
    print(f"📁 Pliki wygenerowane:")
    print(f"   - Audio: {audio_file}")
    print(f"   - Dane JSON: {json_file}")
    print(f"   - Notatki HTML: {html_filename}")

if __name__ == "__main__":
    main()