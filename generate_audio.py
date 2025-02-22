from gtts import gTTS
from pydub import AudioSegment
import tempfile

def generate_audio(script: str) -> str:
    if not script.strip():
        raise ValueError("No script provided for audio conversion.")

    # Generate TTS audio
    textToSpeech = gTTS(text=script, lang="en", tld='ca')  # British English accent
    tempAudioPath = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
    textToSpeech.save(tempAudioPath)

    # Load the generated audio and lower the pitch
    audio = AudioSegment.from_file(tempAudioPath)
    
    audio = audio.normalize()
    audio = audio.fade_in(100).fade_out(100)

    # Export the modified audio
    podcast_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
    audio.export(podcast_path, format="mp3")

    return podcast_path