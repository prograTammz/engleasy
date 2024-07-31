from openai import OpenAI

client = OpenAI()

# Takes a prompt as a string and creates request to Chatgpt 4o
async def create_gpt_completion(user_message: str) -> str:

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": user_message}
        ]
    )

    return response.choices[0].message.content