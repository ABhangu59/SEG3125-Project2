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

def generate_fitness(goal, language):

    if not goal.strip():
        return "Please provide a fitness goal and activity level (basic, intermediate, active) to generate an action plan."
    messages = [
        {
            "role": "system",
            "content": 
            """
            You are a supportive and empathetic personal trainer or fitness guru. You will generate a structured table that contains a weekly workout schedule for a given fitness goal and activity level.
            For the schedule you will include
            1) The appropriate days of the week for the specified workout, whether it is a 3-day, 4-day, 5-day, 6-day or 7-day workout plan. Mention the standard Monday-Wednesday-Friday workout plan but keep the label for the days generic like "Day 1".
            2) For each day focus on a different muscle group (back, chest, etc) to prevent fatigue and injury.
            3) Each exercise should include the number of sets and reps relative to the user's fitness capability (i.e. if they are a beginner or more intermediate).
            4) Outside of the table, mention the importance of warm-up exercises, stretching and proper hydration. 
            Cater the language level of the response to the activity level of the user. If they are more advanced, use terms that are more commonly used in the fitness world.
            """
        },
        {
            "role": "user",
            "content": f"Generate a fitness plan for {goal} and respond in the language of the input. Use the locale {language} if needed for dates, measurements or other localization factors."
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

def generate_nutrition(goal, language):
    if not goal.strip():
        return "Please provide a nutrition goal (weight loss, muscle gain, balanced diet) to generate a meal plan."
    messages = [
    {
        "role": "system",
        "content": 
        """
        You are a highly skilled and empathetic nutritionist and dietitian with expertise in meal planning, macronutrient balance, and dietary optimization. 
        Your role is to create a personalized, structured, and macro-based weekly meal plan that aligns with the user's specific dietary goal.

        For the meal plan, you will: 
        1) Generate a 7-day meal plan with detailed food recommendations tailored to the given nutrition goal.
        2) Each day should include Breakfast, Lunch, Dinner, and Snacks, ensuring variety and nutrient balance.
        3) Label the days as "Day 1," "Day 2," etc., in the appropriate language to maintain flexibility while structuring a sustainable plan.
        4) For each meal, suggest portion sizes, macronutrient breakdown (carbs, proteins, fats), and specific food items that align with the user’s goal.
        5) Provide substitutions for common dietary restrictions (e.g., vegetarian, vegan, gluten-free, halal) if needed.

        Personalization Based on Goal:
        1) Weight Loss:
            - Focus on caloric deficit while maintaining high-protein, fiber-rich foods to promote satiety.
            - Incorporate healthy fats (avocados, nuts) and complex carbohydrates (quinoa, sweet potatoes).
            - Recommend low-calorie, nutrient-dense snacks to prevent binge eating.
            - Discuss the importance of not developing an unhealthy relationship with food

        2) Muscle Gain:
            - Prioritize a high-protein diet (lean meats, fish, tofu, eggs).
            - Include pre- and post-workout nutrition recommendations.
            - Ensure progressive caloric surplus with healthy carbs (oats, brown rice) and fats.

        3) Balanced Diet (General Health & Well-being):
            - Emphasize micronutrients (vitamins & minerals) with a diverse range of vegetables, lean proteins, whole grains, and healthy fats.
            - Suggest gut-friendly foods (probiotics, fermented foods).
            - Encourage meal timing strategies for sustained energy levels.

        Output Format:
        - The meal plan should be presented in a clean and structured table.
        - Provide a brief summary below the table to reinforce key takeaways.
        - Use clear, concise language while maintaining a supportive tone.
        - If the user is a beginner, then please use less complex language to make it more inclusive and beginner friendly. 
        """
    },
    {
        "role": "user",
        "content": f"Generate a nutrition plan for {goal} and respond in the language of the input. Use the locale {language} if needed for dates, measurements or other localization factors."    
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

    nutrition_content = ""
    for chunk in completion:
            nutrition_content += chunk.choices[0].delta.content or ""

    return nutrition_content
#--------------------------------------------------------------------------------------------------

# Functions for Text To Speech: 
def generate_engFitness_tts(input):
    queries = [msg[0] for msg in input if msg[0]]
    conversation_text = "\n".join(queries)

    script = generate_script(conversation_text)
    audio_path = generate_audio(script)

    return script, audio_path

def generate_frFitness_tts(input):
    queries = [msg[0] for msg in input if msg[0]]
    conversation_text = "\n".join(queries)

    script = generate_french_script(conversation_text)
    audio_path = generate_audio(script)

    return script, audio_path

def generate_engNutrition_tts(input):
    queries = [msg[0] for msg in input if msg[0]]
    conversation_text = "\n".join(queries)

    script = generate_nutrition_tts(conversation_text)
    audio_path = generate_audio(script)

    return script, audio_path

def generate_frNutrition_tts(input):
    queries = [msg[0] for msg in input if msg[0]]
    conversation_text = "\n".join(queries)

    script = generate_french_nutrition_tts(conversation_text)
    audio_path = generate_audio(script)

    return script, audio_path
# -------------------------------------------------------------------------

# HTML & JS Elements: 
TITLE = """ 
<h1>Welcome to GainsGPT! </h1>
<p>A state of the art chatbot who will help you reach your fitness goals and dream physique! </p>

<p>Ask the AI Chatbot about creating fitness plans, defining workout goals or providing information about dietary requirements</p>

<ul> 
<li>Don't forget to check out the other two tabs</li>
<li>Check out GainsGPT Fitness Plan Generator to make a fitness plan tailored to your specific needs </li>
<li>Check out GainsGPT Nutrition Guide for any nutrition inquiries you may have to get to your fitness goals! </li>
</ul>


"""

TITLE2 = """ 
<h1>GainsGPT 💪🏼 Fitness Plan Generator</h1>
<p>Include the appropriate days of the week for the specified workout, whether it is a 3-day, 4-day, 5-day, 6-day or 7-day workout plan</p>

<p> Please specify your fitness level [beginner, intermediate, advanced] and GainsGPT will generate a workout plan for you!</p>
<p>Generate a structured table that contains a weekly workout schedule for a given fitness goal and activity level</p>
<hr>

"""
TITLE3 = """ 
<h1>GainsGPT Nutrition Guide</h1>
<p>Please provide any dietary restrictions (e.g., vegetarian, vegan, gluten-free, halal) you have to GainsGPT </p>
"""

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
with gr.Blocks(fill_width=True,theme=gr.themes.Soft(primary_hue="emerald", secondary_hue="yellow"), js=js, css = CSS) as demo:
    hidden_lang = gr.Textbox(visible=False, elem_id="hidden-lang-box")
    gr.Image("image.jpg", show_label=False, show_download_button = False, show_fullscreen_button = False)
    with gr.Tabs():
        # General Chatbot: 
        with gr.TabItem("Inquire About Health"):
            gr.HTML(TITLE)
            chatbot = gr.Chatbot(label="Got Any Questions? 💪🏼")
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
                    fitness_input = gr.Textbox(
                        label="Fitness Goal!",
                        placeholder="Let GainsGPT know your activity level and how many days you want to work out",
                        lines=1
                        )
                    send_button = gr.Button("Show Me The Gains 🏋️‍♀️", variant="secondary", elem_id="send-btn")  # Send button with an icon
            with gr.Row():
                with gr.Accordion(label="Some Questions You Can Ask:"):
                    example_questions = [
                            ["What's a good workout plan for beginners?"],
                            ["How can I build muscle effectively?"],
                            ["What are the best exercises for fat loss?"],
                            ["What’s a good workout split for a 4-day routine?"],
                            ["What’s the best way to recover after a tough workout?"],
                            ["Is cardio necessary for weight loss?"],
                            ["Can I build muscle with just bodyweight exercises?"],
                            ["How do I prevent injuries while working out?"],
                            ["As a beginner, whats 5 day routine I can use to get started on my fitness journey?"],

                        ]
                    gr.Examples(examples=example_questions, inputs=[fitness_input])
            with gr.Row():
                fitness_output = gr.Markdown("### Your Fitness Plan Will Appear Here, Get Ready For The Gains!", elem_id="fitness-markdown")
                # Submit via Enter key or clicking the button
                fitness_input.submit(
                    fn=lambda goal, lang: "Generating your fitness plan... ⏳" if goal.strip() else "Please provide a fitness goal first.",
                    inputs=[fitness_input,hidden_lang],
                    outputs=fitness_output
                ).then(
                    fn=generate_fitness,
                    inputs=[fitness_input,hidden_lang],
                    outputs=fitness_output
                ).then(
                    fn=lambda: "",
                    inputs=None,
                    outputs=fitness_input
                )
                send_button.click(
                    fn=lambda goal, lang: "Generating your fitness plan... ⏳" if goal.strip() else "Please provide a fitness goal first.",
                    inputs=[fitness_input,hidden_lang],
                    outputs=fitness_output
                ).then(
                    fn=generate_fitness,
                    inputs=[fitness_input,hidden_lang],
                    outputs=fitness_output
                ).then(
                    fn=lambda: "",
                    inputs=None,
                    outputs=fitness_input
                )
            with gr.Row():
                gr.HTML("<br> <hr> <br> <h2>Listen On The Go With Our Text To Speech Functionality</h2>")
            with gr.Row():
                podcast_output = gr.Textbox(label="Behind The Scenes of Your Fitness Plan in Audio Form:", placeholder="A readable script will appear here!", interactive = False)
            with gr.Row():
                audio_output = gr.Audio(label="Want To Listen To Your Fitness Plan?")
            with gr.Row():
                podcast_button = gr.Button("Generate English Podcast Script and Audio")
                podcast_button.click(
                    fn=generate_engFitness_tts,
                    inputs=fitness_output,
                    outputs=[podcast_output, audio_output]
                )
                fr_pod_button = gr.Button("Generate French Podcast Script and Audio")
                fr_pod_button.click(
                    fn=generate_frFitness_tts,
                    inputs=fitness_output,
                    outputs=[podcast_output, audio_output]
                )
        # Nutrition Page 
        with gr.TabItem("Generate Nutrition Plan"):
            gr.HTML(TITLE3)

            with gr.Row():
                with gr.Column():
                    nutrition_input = gr.Textbox(
                        label="Nutrition Goal!",
                        placeholder="Let GainsGPT know your nutrition goal and your dietary restrictions/preferences",
                        lines=1
                        )
                    send_button = gr.Button("Show Me The Food 🥬", variant="secondary", elem_id="send-btn")  # Send button with an icon

            with gr.Row():
                with gr.Accordion(label="Some Quick Questions You Can Ask:"):
                    example_questions = [
                            ["Can you help me create a 7-day meal plan for weight loss?"],
                            ["What are some healthy snacks I can include in my diet?"],
                            ["I want to gain muscle. What should my meal plan look like?"],
                            ["What are some vegetarian options for my weekly meal plan?"],
                            ["How can I ensure I get enough protein in a vegan diet?"],
                            ["Can you provide a balanced meal plan for general health?"],
                            ["What are some gut-friendly foods I should include?"],
                            ["How do I calculate portion sizes for my meals?"],
                            ["Can you help me substitute gluten-free options in my meal plan?"],
                            ["What are some low-calorie snacks that are high in protein?"],
                            ["What’s a simple meal plan for beginners focusing on healthy eating?"],
                            ["How can I manage my cravings while on a diet?"]
                        ]

                    gr.Examples(examples=example_questions, inputs=[nutrition_input])
            with gr.Row():
                nutrition_output = gr.Markdown("### Your Nutrition Plan Will Appear Here, Get Ready For The Yum!", elem_id="nutrition-markdown")
                # Submit via Enter key or clicking the button
                nutrition_input.submit(
                    fn=lambda goal, lang: "Generating your nutrition plan... ⏳" if goal.strip() else "Please provide a nutrition goal first.",
                    inputs=[nutrition_input,hidden_lang],
                    outputs=nutrition_output
                ).then(
                    fn=generate_nutrition,
                    inputs=[nutrition_input,hidden_lang],
                    outputs=nutrition_output
                ).then(
                    fn=lambda: "",
                    inputs=None,
                    outputs=nutrition_input
                )

                send_button.click(
                    fn=lambda goal, lang: "Generating your nutrition plan... ⏳" if goal.strip() else "Please provide a nutrition goal first.",
                    inputs=[nutrition_input,hidden_lang],
                    outputs=nutrition_output
                ).then(
                    fn=generate_nutrition,
                    inputs=[nutrition_input,hidden_lang],
                    outputs=nutrition_output
                ).then(
                    fn=lambda: "",
                    inputs=None,
                    outputs=nutrition_input
                )
            with gr.Row():
                gr.HTML("<br> <hr> <br> <h2>Listen On The Go With Our Text To Speech Functionality</h2>")
            with gr.Row():
                podcast_output = gr.Textbox(label="Behind The Scenes of Your Nutrition Plan in Audio Form:", placeholder="A readable script will appear here!", interactive = False)
            with gr.Row():
                audio_output = gr.Audio(label="Want To Listen To Your Nutrition Plan?")
            with gr.Row():
                podcast_button = gr.Button("Generate English Podcast Script and Audio")
                podcast_button.click(
                    fn=generate_engNutrition_tts,
                    inputs=nutrition_output,
                    outputs=[podcast_output, audio_output]
                )
                fr_pod_button = gr.Button("Generate French Podcast Script and Audio")
                fr_pod_button.click(
                    fn=generate_frNutrition_tts,
                    inputs=nutrition_output,
                    outputs=[podcast_output, audio_output]
                )
# ----------------------------------------------------------------------------

# Launching the app:
if __name__ == "__main__":
    demo.launch()