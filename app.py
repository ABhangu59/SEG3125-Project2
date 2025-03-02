import gradio as gr
from groq import Groq
from dotenv import load_dotenv
import os
from generate_audio import generate_audio
from script_generator import generate_script, generate_french_script, generate_french_nutrition_tts, generate_nutrition_tts

load_dotenv()

api_key = os.getenv("api_key")
# Initialize Groq client
client = Groq(api_key=api_key)

conversation_history = []

# Functions for setting up the different chatbot streams
def chatbot_stream(user_input):
    global conversation_history
    conversation_history.append({"role": "user", "content": user_input})

    # Add a system message if the history is empty
    if len(conversation_history) == 1:
        conversation_history.insert(0, {
            "role": "system",
            "content": "You are an expert on personal training, nutrition and fitness. Provide concise, structured and insightful respones to general queries about fitness, working out or general dietary goals"
        })

    # Turning on the big ol AI brain 
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=conversation_history,
        temperature=1,
        max_completion_tokens=1024,
        top_p=1, 
        stream=True,
        stop=None,
    )

    response_content = ""
    for chunk in completion:
        response_content += chunk.choices[0].delta.content or ""


    conversation_history.append({"role": "assistant", "content": response_content})
    
    return [(msg["content"] if msg["role"] == "user" else None, 
            msg["content"] if msg["role"] == "assistant" else None) 
            for msg in conversation_history]

def generate_fitness(goal, activity_level, days_per_week, language):

    if not goal.strip():
        return "Please provide a fitness goal and activity level (basic, intermediate, active) to generate an action plan."
    messages = [
        {
            "role": "system",
            "content": 
            """
            You are a supportive and empathetic personal trainer or fitness guru. You will generate a structured table that contains a weekly workout schedule for a given fitness goal and activity level.
            For the schedule you will include
            1) The appropriate days of the week for the specified workout, whether it is a 3-day, 4-day, 5-day, 6-day or 7-day workout plan. Make the labels generic instead of listing specific days of the week.
            2) For each day focus on a different muscle group (back, chest, etc) to prevent fatigue and injury.
            3) Each exercise should include the number of sets and reps relative to the user's fitness capability.
            4) Outside of the table, mention the importance of warm-up exercises, stretching and proper hydration. 
            Cater the language level of the response to the activity level of the user. If they are more advanced, use terms that are more commonly used in the fitness world.
            """
        },
        {
            "role": "user",
            "content": f"Generate a fitness plan for {goal} given a {activity_level} experience level where workouts occur {days_per_week} per week. Respond in the language of the input and use the locale {language} if needed for dates, measurements or other localization factors."
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

    fitness_content = ""
    for chunk in completion:
        fitness_content += chunk.choices[0].delta.content or ""

    return fitness_content

#--------------------------------------------------------------------------------------------------

# Functions for Text To Speech: 
def generate_engFitness_tts(input):
    queries = [msg[0] for msg in input if msg[0]]
    conversation_text = "\n".join(queries)

    script = generate_script(conversation_text)
    audio_path = generate_audio(script)

    return audio_path

def generate_frFitness_tts(input):
    queries = [msg[0] for msg in input if msg[0]]
    conversation_text = "\n".join(queries)

    script = generate_french_script(conversation_text)
    audio_path = generate_audio(script)

    return audio_path
# -------------------------------------------------------------------------

# HTML & JS Elements: 

TITLE2 = """ 
<h1>GainsGPT 💪🏼 Fitness Plan Generator</h1>
<p>Include the appropriate days of the week for the specified workout, whether it is a 3-day, 4-day, 5-day, 6-day or 7-day workout plan</p>

<p> Please specify your fitness level [beginner, intermediate, advanced] and GainsGPT will generate a workout plan for you!</p>
<p>Generate a structured table that contains a weekly workout schedule for a given fitness goal and activity level</p>
<hr>

"""

initial_prompt = [
    (None, "Welcome to GainsGPT!\n\nA state of the art chatbot who will help you reach your fitness goals and dream physique!\n\nAsk GainsGPT if you have questions about working out, need tips on stretching, or want advice on nutrition and recovery. 💪"),
    (None, "Don't forget to check out the GainsGPT Fitness Plan Generator to make a fitness plan tailored to your specific needs!")
    ]

js = """
function setUserLanguage() {
        let userLang = navigator.language || navigator.userLanguage;
        const hiddenLangTextarea = document.querySelector('#hidden-lang-box textarea');
        hiddenLangTextarea.value = userLang;

        console.log(hiddenLangTextarea.value)
    }
"""

CSS = """
body { 
background-color: #f0f0f0;
}


"""


# ----------------------------------------------------------------------------

# Gradio Interface: 
with gr.Blocks(theme=gr.themes.Soft(primary_hue="emerald", secondary_hue="yellow"), js=js, css = CSS) as demo:
    
    with gr.Tabs():
        # General Chatbot: 
        with gr.TabItem("Inquire About Health"):
            with gr.Row():
                hidden_lang = gr.Textbox(visible=False, elem_id="hidden-lang-box")
                gr.Image("gainsgpt-banner.png", show_label=False, show_download_button = False, show_fullscreen_button = False, height="10rem")
            # with gr.Row():
            #     gr.HTML(TITLE)
            with gr.Row():
                chatbot = gr.Chatbot(label="Got Any Questions? 💪🏼", value=initial_prompt)
            with gr.Row(equal_height=True, height=60):
                user_input = gr.Textbox(
                        placeholder="Type your question here...",
                        lines=1,
                        show_label=False,
                        elem_classes="user-in-chatbot1",
                        scale=1
                    )
                send_button = gr.Button("Ask", elem_classes="btn-1", scale=0)

                # Chatbot functionality: Update chatbot and clear text input
                send_button.click(
                    fn=chatbot_stream,  
                    inputs=user_input,
                    outputs=chatbot,
                    queue=True  # Enables streaming responses
                ).then(
                    fn=lambda: "",  # Clear the input box after sending
                    inputs=None,
                    outputs=user_input
                )
        # Fitness Tab: 
        with gr.TabItem("Generate Fitness Plan"):
            gr.HTML(TITLE2)
            with gr.Row():
                with gr.Column():
                    activity = gr.Radio(["Beginner","Intermediate","Advanced"], label="Activity Level")
                with gr.Column():
                    days_per_week = gr.Dropdown(
                        ["1 Day", "2 Days", "3 Days (recommended)", "4 Days", "5 Days", "6 Days", "7 Days"],
                        interactive=True
                    )
            with gr.Row():
                with gr.Column():
                    fitness_input = gr.Textbox(
                        label="Fitness Goal!",
                        placeholder="Let GainsGPT know your activity level and how many days you want to work out",
                        lines=1
                        )
                    send_button = gr.Button("Show Me The Gains 🏋️‍♀️", variant="secondary", elem_id="send-btn")  # Send button with an icon
            with gr.Row():
                with gr.Accordion(label="Some Questions You Can Ask:"):
                    example_questions = [
                    ["What’s the best workout plan to lose 2 lbs per week?"],
                    ["How can I build muscle while keeping my body fat under 15%?"],
                    ["What exercises are most effective for lowering blood pressure?"],
                    ["What’s an optimal 4-day workout routine to improve heart health?"],
                    ["How can I recover faster to maintain a consistent fat loss routine?"],
                    ["Is cardio necessary to lose 1.5 lbs per week, or can I rely on strength training?"],
                    ["What are the best workouts to prevent injuries while training for weight loss?"],
                    ["As a beginner, I would like lose 10 lbs in two months and improve endurance, how can I go about this??"]
                ]
                    gr.Examples(examples=example_questions, inputs=[fitness_input])
            with gr.Row():
                fitness_output = gr.Markdown("### Your Fitness Plan Will Appear Here, Get Ready For The Gains!", elem_id="fitness-markdown")
                # Submit via Enter key or clicking the button
                fitness_input.submit(
                    fn=lambda goal, lang, activity, days_of_week: "Generating your fitness plan... ⏳" if goal.strip() else "Please provide a fitness goal first.",
                    inputs=[fitness_input, activity, days_per_week, hidden_lang],
                    outputs=fitness_output
                ).then(
                    fn=generate_fitness,
                    inputs=[fitness_input, activity, days_per_week, hidden_lang],
                    outputs=fitness_output
                ).then(
                    fn=lambda: "",
                    inputs=None,
                    outputs=fitness_input
                )
                send_button.click(
                    fn=lambda goal, lang: "Generating your fitness plan... ⏳" if goal.strip() else "Please provide a fitness goal first.",
                    inputs=[fitness_input, activity, days_per_week, hidden_lang],
                    outputs=fitness_output
                ).then(
                    fn=generate_fitness,
                    inputs=[fitness_input, activity, days_per_week, hidden_lang],
                    outputs=fitness_output
                ).then(
                    fn=lambda: "",
                    inputs=None,
                    outputs=fitness_input
                )
            with gr.Row():
                gr.HTML("<br> <hr> <br> <h2>Listen On The Go With Our Text To Speech Functionality</h2>")
            with gr.Row():
                audio_output = gr.Audio(label="Want To Listen To Your Fitness Plan?")
            with gr.Row():
                podcast_button = gr.Button("Listen to an English Fitness Plan")
                podcast_button.click(
                    fn=generate_engFitness_tts,
                    inputs=fitness_output,
                    outputs=audio_output
                )
                fr_pod_button = gr.Button("Listen to a French Fitness Plan")
                fr_pod_button.click(
                    fn=generate_frFitness_tts,
                    inputs=fitness_output,
                    outputs=audio_output
                )
# ----------------------------------------------------------------------------

# Launching the app:
if __name__ == "__main__":
    demo.launch()