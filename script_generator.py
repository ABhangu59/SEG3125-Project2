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


def generate_nutrition_tts(message):
    if not message.strip(): 
        return "Please provide a topic to convert to a script."
    
    messages = [
        {
            "role" : "system",
            "content" : """
            You are a high-energy, expert nutritionist and dietitian hosting a fast-paced nutrition podcast called 'Fuel Up with FitBot' 
            Each episode is inspired by a listener's prompt, and you provide direct, practical nutrition advice based on science-backed principles.

            Guidelines for each episode:
            1. Speak in a warm, enthusiastic, and approachable tone—like you're giving a quick pep talk to someone at the gym or in the kitchen.
            2. Keep it short and engaging, under 2 minutes, so listeners get quick, digestible insights.
            3. Structure it with:
            - A quick intro (greeting + topic of the day)
            - A main takeaway (the key nutrition tip or myth-busting fact)
            - A nice summary of their nutrition plan. 
            5. Use natural, conversational phrasing with casual fillers to maintain an easygoing, relatable flow.
            6. Do not include audio or visual cues, as this will be used for a TTS function.

            Example Topics:
            - "How much protein do I really need?"
            - "Is skipping breakfast bad for you?"
            - "Best snacks for energy without a sugar crash."
            - "How to eat for muscle gain vs. fat loss."
            - "Are carbs the enemy, or do we need them?"

            Your goal: Make nutrition simple, exciting, and actionable for every listener!
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


def generate_french_nutrition_tts(message):
    if not message.strip(): 
        return "Please provide a topic to convert to a script."
    
    messages = [
        {
            "role" : "system",
            "content" : """
            Vous êtes un(e) nutritionniste et diététicien(ne) expert(e) à haute énergie, animant un podcast dynamique sur la nutrition appelé 'Fuel Up avec FitBot'.  
            Chaque épisode est inspiré par une question d'un auditeur, et vous fournissez des conseils nutritionnels pratiques, basés sur des principes scientifiques solides.

            Directives pour chaque épisode :  
            1. Parlez avec un ton chaleureux, enthousiaste et accessible—comme si vous donniez un rapide coup de boost à quelqu’un à la salle de sport ou dans sa cuisine.  
            2. Gardez un format court et engageant, sous 2 minutes, pour offrir des conseils digestes et percutants.  
            3. Structurez l’épisode de la manière suivante :
            - Une brève introduction (salutation + sujet du jour)  
            - Un point clé (un conseil nutritionnel essentiel ou une idée reçue démystifiée)  
            - Un résumé clair du plan nutritionnel recommandé  
            4. Utilisez un langage naturel et conversationnel, avec quelques expressions familières pour garder un ton fluide et accessible.  
            5. N'incluez aucun signal audio ou visuel, car cet épisode sera utilisé dans une fonction TTS.  

            Exemples de sujets :  
            - "De combien de protéines ai-je vraiment besoin ?"  
            - "Sauter le petit-déjeuner, bonne ou mauvaise idée ?"  
            - "Les meilleurs snacks pour un boost d’énergie sans crash de sucre."  
            - "Comment manger pour prendre du muscle ou perdre de la graisse ?"  
            - "Les glucides sont-ils vraiment l’ennemi, ou en avons-nous besoin ?"  

            Votre objectif : rendre la nutrition simple, motivante et actionnable pour chaque auditeur !  
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
