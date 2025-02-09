from flask import Flask, render_template, request
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Load OpenAI API key securely from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET", "POST"])
def index():
    result = None  # Variable to store the generated interpretation
    if request.method == "POST":
        prompt = request.form["prompt"]  # Get user input from form
        try:
            # Call OpenAI API for interpretation of the dream description
            response = openai.chat.completions.create(
                model="gpt-4o-mini",  # Specify OpenAI model
                messages=[{
                    "role": "system", "content": "You are an expert in Jungian dream analysis."
                }, {
                    "role": "user", "content": prompt
                }],
                temperature=0.7,
                max_tokens=150
            )
            # Retrieve and store the generated interpretation from the response
            result = response.choices[0].message.content
        except Exception as e:
            result = f"Error: {str(e)}"  # Handle any API errors

    # Render the HTML template and pass the interpretation result
    return render_template("index.html", result=result)

# Run the app locally (Step 3)
if __name__ == "__main__":
    app.run(debug=True)  # Run the app locally for testing
