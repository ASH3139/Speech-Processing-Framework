# SPF — Smart Car AI  |  Multilingual Voice Assistant

## Languages Supported
| Language | Voice Commands | Responses |
|---|---|---|
| English | ✅ | ✅ |
| Hindi   | ✅ (romanised) | ✅ |
| Telugu  | ✅ (romanised) | ✅ |
| Spanish | ✅ | ✅ |

## Project Structure
```
SPF_Final/
├── api.py            ← Flask server (run this)
├── language.py       ← Language detection + multilingual responses (NEW)
├── intent_model.py   ← LSTM trained on EN+HI+TE+ES phrases
├── entity.py         ← Multilingual entity extractor
├── action.py
├── context.py
├── preprocess.py
├── speech.py
├── wakeword.py
├── requirements.txt
└── templates/
    └── dashboard.html ← Full UI with 4-language mic support
```

## Install
```bash
pip install flask flask-cors speechrecognition pyttsx3 nltk tensorflow pyaudio
```

If NLTK errors on first run:
```python
import nltk; nltk.download('punkt'); nltk.download('punkt_tab')
```

## Run
```bash
python api.py
```
Open: **http://localhost:5000** (Chrome or Edge)

## Example Voice Commands

### English
- "Set temperature to 24 degrees"
- "Open the window"
- "Play music"
- "Navigate to home"
- "Call mom"

### Hindi
- "Temperature 24 karo"
- "Khidki kholo"
- "Gaana bajao"
- "Ghar chalo"
- "Maa ko call karo"

### Telugu
- "Temperature 24 cheyyi"
- "Kiddiki teruvu"
- "Paata veyyi"
- "Illu ki vellu"
- "Amma ki call cheyyi"

### Spanish
- "Pon la temperatura a 24"
- "Abre la ventana"
- "Pon musica"
- "Navega a casa"
- "Llama a mama"

## How Language Detection Works
1. Browser's Web Speech API runs 4 recognizers in parallel (EN/HI/TE/ES)
2. First one to get a result wins
3. Flask's `language.py` scores keyword matches to confirm language
4. Response is generated in the detected language
5. Memory panel shows detected language with flag
