import openai
import os

openai.api_key = os.environ.get("OPENAI_API_KEY")


def ask_gpt3(prompt):
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=300,
        n=1,
        stop=None,
        temperature=0.5,
    )

    return response.choices[0].text.strip()
