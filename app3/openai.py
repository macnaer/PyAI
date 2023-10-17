import openai
from api_secret import API_KEY_OPENAI

openai.api_key = API_KEY_OPENAI


def ask(prompt):
    return "AI answer: "

    res = openai.Completion.create(
        engine="text-davinchi-002",
        prompt=prompt
    )

    return res["choices"][0]["text"]
