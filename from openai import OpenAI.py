from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "What is an AI agent? (2 sentences)"}]
)

print(response.choices[0].message.content)