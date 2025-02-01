import json
from ics import Calendar, Event
from datetime import datetime

'''
Converts JSON data to an ICS file format.
Takes in the cherry picked events json data and converts it to an ICS file format.

:param json_string: The JSON data containing the events to be converted to ICS.
:return: The ICS calendar object.
'''
def json_to_ics(json_string: str):
    # Parse JSON data
    json_data = json.loads(json_string)


    # Cherry pick what events to include in the calendar
    # Create a new calendar
    cal = Calendar()

    # Add events to the calendar
    for event_data in json_data:
        event = Event()

        # Add event name
        event.name = event_data["event"]

        # Add location and description if available
        if event_data["location"] != "None":
            event.location = event_data["location"]
        if event_data["event_details"] != "None":
            event.description = event_data["event_details"]

# {
#     "events": [
#         {
#             "event": "Event Name",
#             "start_date": "YYYY-MM-DD HH:mm",
#             "end_date": "YYYY-MM-DD HH:mm",
#             "location": "Event location",
#             "event_details": "Event details."
#         }
#     ]
# }
        # Add date and time
        event.begin = datetime.strptime(event_data["start_date"], "%Y-%M-%D %H:%m")

        if "end_date" != "None":
            event.end = datetime.strptime(event_data["end_date"], "%Y-%M-%D %H:%m")
        elif "end_date" == "All Day":
            event.end = datetime.strptime(event_data["start_date"], "%Y-%M-%D %H:%m")
        else: # Default duration is 1 hour
            event.duration = event_data[{"hours": 1}]

        cal.events.add(event)

    return cal


'''
Writes the ICS calendar to a file.

:param cal: The ICS calendar to be written to a file.
:param file_name: The name of the file to write the calendar to.
:return: None
'''
def write_ics(cal: Calendar, file_name: str = "calendar") -> None:
    try:
        # Save the calendar to an .ics file
        with open(f"{file_name}.ics", "w") as f:
            f.write(cal.serialize()) # Write the calendar to the file in the iCalendar format (ICS)
    except Exception as e:
        raise e("An error occurred while writing the ICS file") # Raise an error if an exception occurs
