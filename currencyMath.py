import os
import json
import requests
from openai import OpenAI
from dotenv import load_dotenv
from response_monitor import record_response

# Load API key (for OpenAI only)
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = "gpt-4o"

# 1. Real-time currency conversion using Frankfurter API
def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    try:
        url = f"https://api.frankfurter.app/latest?amount={amount}&from={from_currency}&to={to_currency}"
        response = requests.get(url, timeout=10)
        res = response.json()
        print("🌐 API response:", res)

        if "rates" not in res or to_currency.upper() not in res["rates"]:
            return "❌ Could not retrieve conversion rate."

        converted = round(res["rates"][to_currency.upper()], 2)
        return f"{amount} {from_currency.upper()} is {converted} {to_currency.upper()} at the current rate."

    except requests.exceptions.RequestException as e:
        return f"❌ Request error: {str(e)}"
    except Exception as e:
        return f"❌ Unexpected error: {str(e)}"

# 2. Tool schema
tools = [
    {
        "type": "function",
        "function": {
            "name": "convert_currency",
            "description": "Convert currencies using real-time exchange rates.",
            "parameters": {
                "type": "object",
                "properties": {
                    "amount": {"type": "number", "description": "Amount of money"},
                    "from_currency": {"type": "string", "description": "Currency code to convert from"},
                    "to_currency": {"type": "string", "description": "Currency code to convert to"}
                },
                "required": ["amount", "from_currency", "to_currency"]
            }
        }
    }
]

# 3. LLM logic
def get_response(user_input: str):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful currency conversion assistant. "
                    "When the user asks to convert one currency to another, "
                    "always use the `convert_currency` tool to get the live rate. "
                    "Then respond with only that result in a natural and helpful tone."
                )
            },
            {"role": "user", "content": user_input}
        ],
        tools=tools,
        tool_choice="auto"
    )

    message = response.choices[0].message

    if message.tool_calls:
        tool_call = message.tool_calls[0]
        name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)

        print("🧠 Tool Call Detected:", tool_call.function)

        if name == "convert_currency":
            result = convert_currency(**args)
            print("🧪 Tool Output:", result)

            final_response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "user", "content": user_input},
                    message,
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result
                    }
                ],
                tools=tools,
                tool_choice="none"
            )

            final_message = final_response.choices[0].message.content or result
            record_response(None, user_input, final_response)
            return final_message
        else:
            return "❌ Tool not implemented."

    else:
        record_response(None, user_input, response)
        return message.content

def chat_loop():
    print("💬 Currency ChatBot (Frankfurter edition). Type 'exit' to quit.")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("👋 Goodbye!")
            break

        try:
            answer = get_response(user_input)
            print("Assistant:", answer)
        except Exception as e:
            print("⚠️ Error:", e)

if __name__ == "__main__":
    chat_loop()
