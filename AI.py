import g4f
from g4f.client import Client
import geocoder
import asyncio

if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

def getText():
    return("Spartahack Closing Ceramony, 02-02-2025, 4pm")

location = geocoder.ip('me').city
agent =  Client()

text = getText()

response = agent.chat.completions.create(
    model="gpt-4o",
    messages = [{"role": "system", "content": (f"Your only purpose is to convert text into an ics file format, nothing else, throw an error if there's not enough information, use judgement to find out what format the date is in and time, if no timezone is given, assume based off this location: {location}, do not send unneccacary information, only the ics file format, no embeds either because your response will be used as a string inserted into a file, don't use '`' at all either, if there is no event title/description use the date/time in MM-DD-YYYY HH:MM format as the title, however only use this if there is no event information")}, {"role": "user", "content": text}],
    web_search = False
)

filename = agent.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "system", "content": "your only purpose is to generate a filename for an ICS file (without .ics, or backslash n, NO BACKSLASH N AT ALL IT WILL RUIN THE FILE, NO NEW LINE) based off the information provided, the onlything you will send is a filename NOTHING ELSE, no embeds, no '`' just a filename"}, {"role": "user", "content": text}],
    web_search=False
)

icsFile = open(f"{filename.choices[0].message.content}.ics", "w")

icsFile.write(response.choices[0].message.content)
icsFile.close()

#print(response.choices[0].message.content)


