import cohere
import os

# Generate a summary using Cohere's chat model
def generate_summary(text):
    co = cohere.ClientV2(api_key=os.getenv("COHERE_KEY"))
    message = f"Generate a concise summary:\n{text}"
    response = co.chat(
        model="command-a-03-2025",
        messages=[{"role": "user", "content": message}],
    )
    return response.message.content[0].text