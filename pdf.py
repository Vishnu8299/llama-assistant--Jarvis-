import os

from groq import Groq

client = Groq(
    api_key=os.environ.get("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"),
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "tell news of today and provide the links of the news display the news date .i need 23-08-2024 news. display the news date",
        }
    ],
    model="llama3-8b-8192",
)

print(chat_completion.choices[0].message.content)