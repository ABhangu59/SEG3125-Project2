from groq import Groq
import os
from dotenv import load_dotenv



load_dotenv()

api_key = os.getenv("api_key")
# Initialize Groq client
client = Groq(api_key=api_key)

def generate_english_message(message):
    if not message.strip(): 
        return "Please generate a fitness plan before trying to use the TTS."
    
    messages = [
        {
            "role" : "system",
            "content" : """
            You are a high-energy, motivational personal trainer and proofreader. Your task is to take a fitness plan as input and modify it so that it is TTS-friendly.
            1. Speak in a warm, energetic, and conversational tone, like you’re hyping up a client before a great workout.
            2. Avoid including formatting artifacts as the text will be read out loud.
            3. Keep it concise and organize the information linearly by each workout day.
            4. Summarize important fitness tips at the end and make it suitable for the user's knowledge level (beginner, intermediate, advanced).
            5. Use casual fillers for a natural, approachable flow, without background music or extra frills.
            6. Avoid audio or visual cues, as this will be passed as an input to a TTS function.            
            """
        },
        {
            "role" : "user",
            "content" : f"{message}"
        }
    ]

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=1,
        max_completion_tokens=1024,
        top_p=1, #controls the diversity, higher values increase divversity while lower values make responses more deterministic
        stream=True,
        stop=None,
    )

    script_content = ""
    for chunk in completion:
            script_content += chunk.choices[0].delta.content or ""

    return script_content


def generate_french_message(message):
    if not message.strip(): 
        return "Veuillez générer un plan de remise en forme avant d'essayer d'utiliser la fonction de synthèse vocale."
    
    messages = [
        {
            "role" : "system",
            "content" : """
            Tu es un entraîneur personnel ultra motivant et un relecteur dynamique. Ta mission est de prendre un programme d'entraînement et de l'adapter pour qu'il soit facile à lire à voix haute avec un logiciel de synthèse vocale (TTS).
            1. Adopte un ton chaleureux, énergique et engageant, comme si tu motivais un client avant une super séance d'entraînement.
            2. Évite les éléments de mise en forme, car le texte sera lu à voix haute.
            3. Sois concis et présente l'information de façon linéaire, jour par jour.
            4. Résume les conseils essentiels à la fin et adapte-les au niveau de l'utilisateur (débutant, intermédiaire, avancé).
            5. Utilise des expressions naturelles et un ton accessible, sans musique de fond ni artifices superflus.
            6. Évite les indices audio ou visuels, car ce texte servira d'entrée pour une fonction TTS.
            """
        },
        {
            "role" : "user",
            "content" : f"{message}"
        }
    ]


    completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=1,
            max_completion_tokens=1024,
            top_p=1, #controls the diversity, higher values increase divversity while lower values make responses more deterministic
            stream=True,
            stop=None,
        )

    script_content = ""
    for chunk in completion:
                script_content += chunk.choices[0].delta.content or ""

    return script_content
