#This file is sponsored by these pachages

import g4f
from g4f.client import Client
import geocoder
import asyncio
import json
import datetime

year = datetime.datetime.now().year


#uhhh chat gpt told me to put this here so the code would function properly
if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

#converts AI response to json format
def str2json(string):
    return json.loads(str(string))

#trust me bro, we don't want to dox you
location = geocoder.ip('me').city

agent =  Client() #without this line, the program wouldn't be possible


#gets the AI response using an extremely professional system prompt to make sure the AI responds correctly
def getResponse(text):
    response = agent.chat.completions.create(
        model="gpt-4o",
        messages = [{"role": "system", "content": (f"""Your only purpose is to convert text into a json file format, nothing else, 
                                                throw an error if there's not enough information, use judgement 
                                                to find out what format the date is in and time, 
                                                if no timezone is given, assume The timezone based off this location: {location}, you may not even need it,
                                                    do not send unneccacary information, only the json file format, 
                                                no embeds either because your response will be used as a string inserted 
                                                into a file, don't use '`' at all either, if there is no event title/description 
                                                use the date/time in MM-DD-YYYY HH:MM format as the title,
                                                however only use this if there is no event information, json format is 'event', 'start_date', 'end date', 
                                                'location", 'event details' in that order and nothing else. if there is no location, 'None'. 
                                                If there is no end date specified put an hour after the time it starts. If there is no end date put at 23:59,
                                                  if there is no year assume the year is {year}, MAKE SURE IT IS IN JSON FORMAT""")},
                                                    {"role": "user", "content": text}],
        web_search = False
    )
    return(response)


#This is the part of the code the other files will use
def getResponseJson(txt0):
    strRespo = getResponse(str(txt0))
    return str2json(strRespo)
