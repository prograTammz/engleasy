from openai import OpenAI

client = OpenAI()

# Takes a prompt as a string and creates request to Chatgpt 4o
async def create_gpt_completion(prompt: str) -> str:

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "assistant", "content": prompt}
        ]
    )

    return response.choices[0].message.content