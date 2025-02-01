import pytesseract
from PIL import Image
import AI

# Load an image
image = Image.open('image.png')

# Perform OCR on the image
text = pytesseract.image_to_string(image)
AI.stuff(text) # Print the text extracted from the image




# Interface with AI agent to get the dates into a json file

import json
from ics import Calendar, Event
from datetime import datetime

# Your JSON data
json_data = '''
{
  "events": [
    {
      "event": "Out of Office",
      "start_date": "2025-02-03",
      "end_date": "2025-02-07",
      "time": "All day",
      "notes": "No access to email during this period."
    },
    {
      "event": "Express Advising",
      "date": "2025-02-12",
      "time": "1:00 PM - 4:00 PM",
      "location": "In-person at Wilson G-60",
      "notes": "For quick questions only."
    },
    {
      "event": "Summer Transfer Courses Info Session",
      "date": "2025-02-10",
      "time": "3:00 PM - 4:00 PM",
      "notes": "Learn more about signing up for summer courses from other schools and transferring credits back to MSU. Register online."
    },
    {
      "event": "College of Engineering Admissions Info Session",
      "date": "2025-02-18",
      "time": "Unknown",
      "notes": "Learn more about the process and requirements to apply for admission to the College of Engineering at MSU."
    }
  ]
}
'''




# Parse JSON data
data = json.loads(json_data)

# Create a new calendar
cal = Calendar()

# Add events to the calendar
for event_data in data["events"]:
    event = Event()
    event.name = event_data["event"]

    # Handle date and time
    if "start_date" in event_data:  # For multi-day events
        event.begin = datetime.strptime(event_data["start_date"], "%Y-%m-%d")
        event.end = datetime.strptime(event_data["end_date"], "%Y-%m-%d")
    else:  # For single-day events
        event.begin = datetime.strptime(event_data["date"], "%Y-%m-%d")
        if event_data["time"] != "Unknown":
            start_time = datetime.strptime(event_data["time"].split(" - ")[0], "%I:%M %p").time()
            end_time = datetime.strptime(event_data["time"].split(" - ")[1], "%I:%M %p").time()
            event.begin = datetime.combine(event.begin.date(), start_time)
            event.end = datetime.combine(event.begin.date(), end_time)

    # Add location and description
    if "location" in event_data:
        event.location = event_data["location"]
    if "notes" in event_data:
        event.description = event_data["notes"]

    cal.events.add(event)

# Save the calendar to an .ics file
with open("calendar.ics", "w") as f:
    f.write(cal.serialize())

print("Calendar file created: calendar.ics")
