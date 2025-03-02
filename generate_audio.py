from gtts import gTTS
from pydub import AudioSegment
import tempfile

def generate_audio(input: str) -> str:
    if not input.strip():
        raise ValueError("No input provided for audio conversion.")

    # Generate TTS audio
    textToSpeech = gTTS(text=input, lang="en", tld='ca')  # British English accent
    tempAudioPath = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
    textToSpeech.save(tempAudioPath)

    # Load the generated audio and lower the pitch
    audio = AudioSegment.from_file(tempAudioPath)
    
    audio = audio.normalize()
    audio = audio.fade_in(100).fade_out(100)

    # Export the modified audio
    audio_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
    audio.export(audio_path, format="mp3")

    return audio_path