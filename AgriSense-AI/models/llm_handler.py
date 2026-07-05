import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def get_crop_solution(crop_name, problem, language):

    prompt = f"""
You are an expert Agriculture AI Assistant.

Crop Name: {crop_name}
Problem: {problem}

Respond ONLY in {language}.
Do not mix any other language.

Provide the response in the following format:

1. Problem Identification
2. Possible Reason
3. Recommended Solution
4. Prevention Tips

Keep the explanation simple so that farmers can easily understand.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are an experienced agriculture expert who always answers in the user's selected language."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content