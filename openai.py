import openai
from openai import OpenAI
import os

client = OpenAI(api_key=os.environ.get("sk - 0 DZtd5a2niI1kl7g6BpMT3BlbkFJZ66Qd7bKc8nTEAk1vzD5"))

# Set your OpenAI API key here
api_key = ''

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
    {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
  ]
)

print(completion.choices[0].message)
exit()
def ask_openai(prompt):
    try:
        # Sending the prompt to the OpenAI API
        response = Completion.create(
            engine="text-davinci-003",  # You can choose a different model based on your needs
            prompt=prompt,
            max_tokens=150,  # Adjust based on how long you want the response to be
            n=1,  # Number of completions to generate
            stop=None,  # Stop sequence, if any
            temperature=0.7  # Controls randomness. Lower is more deterministic.
        )
        # Extracting the text from the response
        answer = response.choices[0].text.strip()
        return answer
    except Exception as e:
        return f"An error occurred: {str(e)}"


prompt = input("Your prompt here")
response = ask_openai(prompt)
print("OpenAI says:", response)





print(completion.choices[0].message)