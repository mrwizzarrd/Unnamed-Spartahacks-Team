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
    return json.loads(string)

#trust me bro, we don't want to dox you
location = geocoder.ip('me').city

agent =  Client() #without this line, the program wouldn't be possible


'''
Gets the AI response using the GPT-4o model.
Uses custom prompt to get the AI response in the correct json format.

:param text: The text to send to the AI.
:return: The AI response.
'''
def getResponse(text):
    response = agent.chat.completions.create(
        model="gpt-4o",
        messages = [{"role": "system", "content": (f"""YYou are a strict JSON formatter. Your task is to respond with valid JSON in the following format:
                    {{
                        "event": "Event Title",
                        "start_date": "MM-DD-YYYY HH:MM",
                        "end_date": "MM-DD-YYYY HH:MM",
                        "location": "Location",
                        "event_details": "Details"
                    }}. If any of the fields are missing, respond with 'None' where appropriate, and if no event title/description is present, use the date and time in MM-DD-YYYY HH:MM format as the title, unless there is enough information to use as the event title, if not use (Event). The year should default to {year}. The start date and end date should be properly handled with assumed times where applicable (e.g., 23:59 for end time if not specified).
                    Your response **must** be in this format or throw an error. Do not include any extra information or use new lines, backslashes, or other formatting. Ensure everything is enclosed in a valid JSON structure.""")},
                                                    {"role": "user", "content": text}],
        web_search = False
    )
    return(response)

'''
Fixes the JSON string by adding brackets if they are missing.

:param json_string: The JSON string to fix.
:return: The fixed JSON string.
'''
def make_list(json_string):
    if json_string[0] != "[": # Check if the JSON string is a list and fix
        json_string = f"[\n{json_string}]"
    if json_string[-1] != "]":
        json_string = f"{json_string}\n]"
    return json_string


#This is the part of the code the other files will use
def getResponseJson(txt0):
    strRespo = getResponse(txt0).choices[0].message.content
    jsConverted = str2json(strRespo)
    return(jsConverted)
            