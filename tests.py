from ocr import ocr
from json_to_ics import json_to_ics, write_ics

text = ocr("image.png")

json_string = 

ics_data = json_to_ics(json_string)

write_ics(ics_data, "calendar.ics")
