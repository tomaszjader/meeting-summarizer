# Meeting Summarizer 🎯

System do automatycznej transkrypcji i podsumowania spotkań wykorzystujący sztuczną inteligencję OpenAI.

## 📋 Opis

Meeting Summarizer to aplikacja Python, która pozwala na:
- **Nagrywanie spotkań** w czasie rzeczywistym
- **Transkrypcję audio** na tekst przy użyciu OpenAI Whisper
- **Automatyczne podsumowanie** spotkań z wyodrębnieniem kluczowych informacji
- **Generowanie notatek HTML** w profesjonalnym formacie
- **Wysyłanie notatek emailem** do uczestników spotkania
- **Zapisywanie danych** w formacie JSON

## ✨ Funkcjonalności

### 🎙️ Nagrywanie Audio
- Nagrywanie na żywo ze spotkań
- Obsługa istniejących plików audio
- Automatyczne dzielenie dużych plików audio

### 🤖 Sztuczna Inteligencja
- Transkrypcja przy użyciu OpenAI Whisper
- Inteligentne podsumowanie spotkań
- Wyodrębnienie kluczowych tematów
- Identyfikacja zadań do wykonania
- Rozpoznawanie podjętych decyzji

### 📝 Generowanie Dokumentacji
- Profesjonalne notatki HTML
- Eksport danych do JSON
- Czytelny format z sekcjami tematycznymi

### 📧 Komunikacja
- Automatyczne wysyłanie notatek emailem
- Konfigurowalny SMTP
- Wsparcie dla wielu odbiorców

## 🚀 Instalacja

### Wymagania
- Python 3.7+
- Klucz API OpenAI
- Mikrofon (dla nagrywania na żywo)

### Kroki instalacji

1. **Sklonuj lub pobierz projekt**
```bash
git clone <repository-url>
cd meeting-summarizer
```

2. **Zainstaluj zależności**
```bash
pip install -r requirements.txt
```

3. **Skonfiguruj zmienne środowiskowe**

Utwórz plik `.env` w głównym katalogu projektu:
```env
# OpenAI API
OPENAI_API_KEY=your_openai_api_key_here

# Email Configuration (opcjonalne)
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USERNAME=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
```

### Uzyskanie klucza OpenAI API
1. Zarejestruj się na [platform.openai.com](https://platform.openai.com)
2. Przejdź do sekcji API Keys
3. Utwórz nowy klucz API
4. Skopiuj klucz do pliku `.env`

## 📖 Użytkowanie

### Uruchomienie aplikacji
```bash
python mian.py
```

### Opcje użytkowania

**Opcja 1: Nagrywanie nowego spotkania**
- Wybierz opcję "1" w menu
- Podaj czas nagrywania lub naciśnij Enter dla ręcznego zatrzymania
- Aplikacja automatycznie nagra, transkrybuje i podsumuje spotkanie

**Opcja 2: Użycie istniejącego pliku audio**
- Wybierz opcję "2" w menu
- Podaj ścieżkę do pliku audio
- Aplikacja przetworzy plik i utworzy podsumowanie

### Obsługiwane formaty audio
- WAV
- MP3
- M4A
- FLAC
- I inne formaty obsługiwane przez pydub

## 📁 Struktura plików wyjściowych

Po przetworzeniu spotkania aplikacja generuje:

```
meeting_YYYYMMDD_HHMMSS.json    # Dane strukturalne spotkania
notatki_YYYYMMDD_HHMMSS.html    # Notatki w formacie HTML
meeting_audio.wav               # Plik audio (jeśli nagrywano)
```

### Format danych JSON
```json
{
  "summary": "Główne podsumowanie spotkania",
  "key_topics": ["Temat 1", "Temat 2"],
  "action_items": ["Zadanie 1", "Zadanie 2"],
  "decisions": ["Decyzja 1", "Decyzja 2"],
  "next_meeting": {},
  "participants": [],
  "transcript": "Pełna transkrypcja..."
}
```

## ⚙️ Konfiguracja

### Zmienne środowiskowe

| Zmienna | Opis | Wymagane |
|---------|------|----------|
| `OPENAI_API_KEY` | Klucz API OpenAI | ✅ |
| `EMAIL_SMTP_SERVER` | Serwer SMTP | ❌ |
| `EMAIL_PORT` | Port SMTP | ❌ |
| `EMAIL_USERNAME` | Login email | ❌ |
| `EMAIL_PASSWORD` | Hasło email | ❌ |

### Konfiguracja email dla Gmail
1. Włącz uwierzytelnianie dwuskładnikowe
2. Wygeneruj hasło aplikacji
3. Użyj hasła aplikacji w zmiennej `EMAIL_PASSWORD`

## 🛠️ Rozwiązywanie problemów

### Problemy z nagrywaniem audio
- **Windows**: Zainstaluj Microsoft Visual C++ Build Tools
- **macOS**: `brew install portaudio`
- **Linux**: `sudo apt-get install portaudio19-dev`

### Problemy z OpenAI API
- Sprawdź poprawność klucza API
- Upewnij się, że masz wystarczające środki na koncie OpenAI
- Sprawdź limity API

### Problemy z emailem
- Sprawdź konfigurację SMTP
- Dla Gmail użyj hasła aplikacji, nie hasła konta
- Sprawdź ustawienia bezpieczeństwa konta email

## 📦 Zależności

- `openai>=0.27.0` - API OpenAI dla transkrypcji i podsumowania
- `python-dotenv>=1.0.0` - Obsługa plików .env
- `pyaudio>=0.2.11` - Nagrywanie audio
- `pydub>=0.25.1` - Przetwarzanie plików audio

## 🤝 Wkład w projekt

Jeśli chcesz przyczynić się do rozwoju projektu:
1. Utwórz fork repozytorium
2. Stwórz branch dla swojej funkcjonalności
3. Wprowadź zmiany
4. Utwórz Pull Request

## 📄 Licencja

Ten projekt jest dostępny na licencji MIT. Zobacz plik LICENSE dla szczegółów.

## 🆘 Wsparcie

Jeśli napotkasz problemy lub masz pytania:
1. Sprawdź sekcję "Rozwiązywanie problemów"
2. Utwórz issue w repozytorium
3. Skontaktuj się z autorem projektu

---

**Meeting Summarizer** - Automatyzacja dokumentacji spotkań z wykorzystaniem AI 🚀