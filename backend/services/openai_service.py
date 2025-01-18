import openai
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Load API key securely
openai.api_key = os.getenv('OPENAI_API_KEY')

def get_bible_verses(query):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Find Bible verses related to: {query}"}
        ],
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7
    )
    verses = response.choices[0].message['content'].strip().split('\n')
    return [verse.strip() for verse in verses if verse.strip()]
