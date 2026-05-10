import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),
)

INFORMATION_CONTEXT = """
<information_context>
Lapau Bang Jack is a small food court based in Gambir, Jakarta Pusat, DKI Jakarta in front of Istiqlal Mosque.
It sells Padang authentic food.
Available menus are Lontong Tauco, Lontong Cubadak and Pical.
All foods are taste Padang authentic spicy except Lontong Tauco.
Available beverages are only tea and fresh water.
All menus priced for 5000 IDR.
Open from 6 a.m to 12 a.m GMT+7.
Tone should be friendly, simple and local.
</information_context>
"""

SYSTEM_PROMPT = f"""
You are customer service for Lapau Bang Jack.
Always answer in Indonesian language.
Only answer based on this information context:
{INFORMATION_CONTEXT}
When you don't have the information, please say so politely.
Use emojis when appropriate.
"""

messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
]

base_model = os.getenv("BASE_MODEL")

while True:
    user_input = input("User: ")
    user_message = {"role": "user", "content": user_input}

    messages.append(user_message)

    completion = client.chat.completions.create(
        model=base_model,
        messages=messages,
        # max_tokens=50,
    )

    final_output = completion.choices[0].message.content or ""
    print(final_output)

    messages.append({"role": "assistant", "content": final_output})
