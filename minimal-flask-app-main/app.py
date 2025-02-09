from flask import Flask, render_template, request
import openai
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")  # Securely load API key

# Function to generate the Jungian interpretation
def generate_interpretation(dream_description):
    prompt = f"Interpret the following dream based on Carl Jung's psychological theories, focusing on symbolism, archetypes, and the unconscious mind: {dream_description}"
    try:
        response = openai.Completion.create(
            model="text-davinci-003",  # You can use other models like GPT-4
            prompt=prompt,
            max_tokens=300,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error in interpretation: {str(e)}"

# Function to generate the dream-related image using DALL-E
def generate_dream_image(dream_description):
    try:
        response = openai.Image.create(
            prompt=dream_description,
            n=1,
            size="1024x1024"
        )
        return response.data[0].url
    except Exception as e:
        return f"Error generating image: {str(e)}"

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    image_url = None
    if request.method == "POST":
        prompt = request.form["prompt"]
        # Generate Jungian interpretation
        result = generate_interpretation(prompt)
        # Generate corresponding image
        image_url = generate_dream_image(prompt)
    return render_template("index.html", result=result, image_url=image_url)

if __name__ == "__main__":
    app.run(debug=True)  # Run locally for testing
