from ocr import ocr
from json_to_ics import json_to_ics, write_ics
from AI import getResponse

text = ocr("image.png")

json_string = getResponse(text).choices[0].message.content

ics_data = json_to_ics(json_string)

<<<<<<< HEAD
write_ics(ics_data, "calendar3")
=======
write_ics(ics_data, "calendar2")
>>>>>>> c74d4bcdaeb85a776dcc216f6240b2a27931d5f7
