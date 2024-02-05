import openai

API_KEY = open('config', 'r').read()
client = openai.OpenAI(api_key=API_KEY)


def bot_onlineInspectionToolAssistant(message):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "You are an online inspection tool assistant, skilled in analysing websites and generating a diagnosis and a overall rating according to an effective Lead Magnet."},
            {"role": "user", "content": message}
        ]
    )

    print(completion.choices[0].message)
    return completion.choices[0].message
