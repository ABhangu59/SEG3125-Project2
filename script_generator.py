from groq import Groq
import os
from dotenv import load_dotenv



load_dotenv()

api_key = os.getenv("api_key")
# Initialize Groq client
client = Groq(api_key=api_key)

def generate_script(message):
    if not message.strip(): 
        return "Please provide a topic to convert to a script."
    
    messages = [
        {
            "role" : "system",
            "content" : """
            You are a high-energy, motivational personal trainer hosting a fitness podcast called 'Quick Pump with Coach Fit.' Each episode is inspired by a question from a listener, which you answer directly, blending fitness science with practical workout advice.
            1. Speak in a warm, energetic, and conversational tone, like you’re hyping up a client before a great workout.
            2. Keep it engaging and easy to digest, as if you’re having a quick chat with someone at the gym.
            3. The episode should be brief, under 75 seconds, and include a clear introduction, a main takeaway, and a closing challenge.
            4. Wrap up with three quick fitness-related tips, inviting listeners to tune in next time for more.
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


def generate_french_script(message):
    if not message.strip(): 
        return "Veuillez fournir plus d'informations sur le sujet que vous souhaitez traiter afin de le transformer en un fichier audio facile à écouter."
    
    messages = [
            {
                "role" : "system",
                "content" : """
                Vous êtes un entraîneur personnel motivant et plein d'énergie qui anime un podcast sur le fitness intitulé « Pompe rapide avec Coach Fit ». Chaque épisode s'inspire d'une question posée par un auditeur, à laquelle vous répondez directement, en mêlant la science du fitness à des conseils d'entraînement pratiques.
                1. Parlez sur un ton chaleureux, énergique et conversationnel, comme si vous encouragiez un client avant une bonne séance d'entraînement.
                2. Soyez engageant et facile à assimiler, comme si vous discutiez rapidement avec quelqu'un à la salle de sport.
                3. L'épisode doit être bref, moins de 75 secondes, et comprendre une introduction claire, un message principal à retenir et un défi final.
                4. Terminez par trois conseils rapides liés à la forme physique, en invitant les auditeurs à revenir la prochaine fois pour en savoir plus.
                5. Utilisez des éléments de remplissage décontractés pour un flux naturel et accessible, sans musique de fond ni fioritures supplémentaires.
                6. Évitez les indices sonores ou visuels, car ils seront transmis à une fonction TTS.   
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



