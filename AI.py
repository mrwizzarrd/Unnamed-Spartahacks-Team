import g4f
from g4f.client import Client
import geocoder
import asyncio
import json

#<<<<<<< HEAD
if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

def getText():
    return("Spartahack Closing Ceramony, 02-02-2025, 4pm")

def str2json(string):
    return json.loads(string)


location = geocoder.ip('me').city
agent =  Client()

txt = getText()

def getResponse(text):
    response = agent.chat.completions.create(
        model="gpt-4o",
        messages = [{"role": "system", "content": (f"""Your only purpose is to convert text into a json file format, nothing else, 
                                                throw an error if there's not enough information, use judgement 
                                                to find out what format the date is in and time, 
                                                if no timezone is given, assume based off this location: {location},
                                                    do not send unneccacary information, only the json file format, 
                                                no embeds either because your response will be used as a string inserted 
                                                into a file, don't use '`' at all either, if there is no event title/description 
                                                use the date/time in MM-DD-YYYY HH:MM format as the title,
                                                however only use this if there is no event information, json format is 'event', 'start_date', 'end date', 
                                                'location", 'event details' in that order and nothing else. if there is no location, 'None'. 
                                                If there is no end date specified put an hour after the time it starts. If there is no end date put at 23:59""")},
                                                    {"role": "user", "content": text}],
        web_search = False
    )
    return(response)

jsonString = getResponse(txt).choices[0].message.content

"""filename = agent.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "system", "content": "your only purpose is to generate a filename for an ICS file (without .ics, or backslash n, NO BACKSLASH N AT ALL IT WILL RUIN THE FILE, NO NEW LINE) based off the information provided, the onlything you will send is a filename NOTHING ELSE, no embeds, no '`' just a filename"}, {"role": "user", "content": text}],
    web_search=False
)

icsFile = open(f"{filename.choices[0].message.content}.ics", "w")

icsFile.write(response.choices[0].message.content)
icsFile.close()

#print(response.choices[0].message.content)
#=======
def stuff(text):
    location = "Detroit"
    agent =  Client()

    response = agent.chat.completions.create(
        model="gpt-4o",
        messages = [{"role": "system", "content": f"Your only purpose is to convert text into an ics file format, nothing else, throw an error if there's not enough information, use judgement to find out what format the date is in and time, if no timezone is given, assume based off this location: {location}"}, {"role": "user", "content": "uhhhhh"}],
        web_search = False
    )

    print(response.choices[0].message.content)
#>>>>>>> f9a4fd05c19973f2bfb269b3d3a133665b442870"""
