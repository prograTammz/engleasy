from openai import OpenAI


client = OpenAI()

async def get_openai_response(user_message: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": user_message}
        ]
    )
    print(response.choices[0].message.content)
    return response.choices[0].message.content
