from ocr import ocr
from json_to_ics import json_to_ics, write_ics
from AI import getResponse, make_list

# Get text from OCR
text = ocr("image.png")

# Ask chatbot for JSON data
json_string = getResponse(text).choices[0].message.content

# Fix JSON string
json_string = make_list(json_string)

# Convert JSON data to ICS
ics_data = json_to_ics(json_string)

# Write ICS data to file
write_ics(ics_data, "calendar2")

'''
[
    {
        "event": "Out of Office",
        "start_date": "02-03-2025 00:00",
        "end_date": "02-07-2025 23:59",
        "location": "None",
        "event_details": "The user will be out of the office with no access to email during this period."
    },
    {
        "event": "Express Advising",
        "start_date": "02-12-2025 13:00",
        "end_date": "02-12-2025 16:00",
        "location": "Wilson G-60",
        "event_details": "In-person express advising for quick questions."
    },
    {
        "event": "Summer Transfer Courses",
        "start_date": "02-10-2025 15:00",
        "end_date": "02-10-2025 16:00",
        "location": "None",
        "event_details": "Learn more about how to sign up for summer courses from other schools and transfer credits back to MSU."
    },
    {
        "event": "College of Engineering Admissions",
        "start_date": "02-18-2025 00:00",
        "end_date": "02-18-2025 23:59",
        "location": "None",
        "event_details": "Learn more about the process and requirements to apply for admission to the College of Engineering at MSU."
    }
]
'''