import gradio as gr
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("api_key")
# Initialize Groq client
client = Groq(api_key=api_key)

conversation_history = []

# Setting up the AI CHatbot interface
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

def generate_fitness(goal):
    if not goal.strip():
        return "Please provide a fitness goal and activity level (basic, intermediate, active) to generate an action plan."
    messages = [
        {
            "role": "system",
            "content": 
            """
            You are a supportive and empathetic personal trainer or fitness guru. You will generate a structured table that contains a weekly workout schedule for a given fitness goal and activity leve.
            For the schedule you will include
            1) The appropriate days of the week for the specified workout, whether it is a 3-day, 4-day, 5-day, 6-day or 7-day workout plan. Mention the standard Monday-Wednesday-Friday workout plan but keep the label for the days generic like "Day 1".
            2) For each day focus on a different muscle group (back, chest, etc) to prevent fatigue and injury.
            3) Each exercise should include the number of sets and reps relative to the user's fitness capability (i.e. if they are a beginner or more intermediate).
            4) Outside of the table, mention the importance of warm-up exercises and stretching. 
            If the user's activity level is basic,
            - mention tips about time between different sets of an exercise, training until failure, and prioritizing the form of the exercise over the weight.
            - speak in a friendly and encouraging tone.
            Cater the language level of the response to the activity level of the user. If they are more advanced, you can use terms that are more commonly used in the fitness world.
            """
        },
        {
            "role": "user",
            "content": f"{goal}"
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

def generate_nutrition(goal):
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
        3) Label the days as "Day 1," "Day 2," etc., to maintain flexibility while structuring a sustainable plan.
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
        "content": f"{goal}"    
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

    return completion.choices[0].message.content

TITLE = """ 
<h1>AI Chatbot for Personal Training, Nutrition and Fitness</h1>
<p>Ask the AI Chatbot about creating fitness plans, defining workout goals or providing information about dietary requirements</p>
<p>Provide concise, structured and insightful respones to queries</p>
"""

TITLE2 = """ 
<h1>Fitness Plan Generator</h1>
<p>Generate a structured table that contains a weekly workout schedule for a given fitness goal and activity level</p>
<p>Include the appropriate days of the week for the specified workout, whether it is a 3-day, 4-day, 5-day, 6-day or 7-day workout plan</p>
"""

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    with gr.Tabs():
        with gr.TabItem("Inquire About Health"):
            gr.HTML(TITLE)
            chatbot = gr.Chatbot(label="Got Any Questions? 💪🏼")
            with gr.Row():
                user_input = gr.Textbox(
                    label="Your Message",
                    placeholder="Type your question here...",
                    lines=1
                )
                send_button = gr.Button("Ask Question")

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
        with gr.TabItem("Generate Fitness Plan"):
            gr.HTML(TITLE2)
            chaBot = gr.Textbox(label="FitBot")
            with gr.Row():
                fitness_input = gr.Textbox(
                    label="Your Message",
                    placeholder="Type your question here...",
                    lines=1              
                )
                butOn = gr.Button("Ask Question")

                # Chatbot functionality: Update chatbot and clear text input
            butOn.click(
                fn=generate_fitness,  
                inputs=fitness_input,
                outputs=chaBot,
                queue=True  # Enables streaming responses
            ).then(
                fn=lambda: "",  # Clear the input box after sending
                inputs=None,
                outputs=fitness_input
            )


if __name__ == "__main__":
    demo.launch()