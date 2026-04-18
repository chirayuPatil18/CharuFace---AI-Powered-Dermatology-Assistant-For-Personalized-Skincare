import json
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# USER BASED MEMORY FILE
def get_memory_file(email):
    os.makedirs("memory", exist_ok=True)
    return f"memory/{email.replace('@','_')}.json"


def load_memory(email):
    file = get_memory_file(email)

    if not os.path.exists(file):
        return {}

    with open(file, "r") as f:
        return json.load(f)


def save_memory(email, data):
    file = get_memory_file(email)

    with open(file, "w") as f:
        json.dump(data, f, indent=2)


def build_chat_prompt(user_input, memory):

    profile = memory.get("profile", {})
    recommendation = memory.get("recommendation", {})
    history = memory.get("history", [])

    return f"""
You are an expert dermatology AI assistant.

USER PROFILE:
{json.dumps(profile, indent=2)}

PREVIOUS RECOMMENDATION:
{json.dumps(recommendation, indent=2)}

CHAT HISTORY:
{json.dumps(history[-5:], indent=2)}

USER QUESTION:
{user_input}

INSTRUCTIONS:
- Answer dermatology-related queries
- Use previous recommendation when relevant
- Be practical and clear
- Do NOT suggest prescription medicines
"""


def chat_with_ai(user_input, email):

    memory = load_memory(email)

    prompt = build_chat_prompt(user_input, memory)

    response = client.chat.completions.create(
        model="openrouter/auto",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )

    answer = response.choices[0].message.content

    # 🔥 SAVE HISTORY
    memory.setdefault("history", []).append({
        "user": user_input,
        "assistant": answer
    })

    save_memory(email, memory)

    return answer