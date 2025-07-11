import cohere
import os

# Generate 5 numbered questions based on input text using Cohere
def generate_questions(text):
    co = cohere.ClientV2(api_key=os.getenv("COHERE_KEY"))
    message = (f"Generate exactly 5 numbered questions based on the following text. "
               f"Do not include any bullet points, stars, or introductory phrases. "
               f"Just output the 5 questions, each on its own line, numbered 1 to 5:\n\n{text}")
    response = co.chat(
        model="command-a-03-2025",
        messages=[{"role": "user", "content": message}],
    )
    return response.message.content[0].text