import g4f
from g4f.client import Client


location = "Detroit"
agent =  Client()

response = agent.chat.completions.create(
    model="gpt-4o",
    messages = [{"role": "system", "content": f"Your only purpose is to convert text into an ics file format, nothing else, throw an error if there's not enough information, use judgement to find out what format the date is in and time, if no timezone is given, assume based off this location: {location}"}, {"role": "user", "content": "uhhhhh"}],
    web_search = False
)

print(response.choices[0].message.content)