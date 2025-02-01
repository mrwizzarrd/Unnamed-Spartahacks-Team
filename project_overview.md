- # OCR Calendar Creator
	- ## Problem
		- Given an image that contains dates in it, convert it to an `ics` file to be able to import into Google Calendar
	- ## Implementation
		1. User selects to add an image from device (screenshots) or take a new image
		2. Image is sent to OCR, which returns the text
		3. Extracted text from image is sent to language model, which returns a `json`
		4. User selects which events to keep, which updates the `json` string
		5. Finalized `json` string is sent to a `json` to `ics` creator
		6. User can download the `ics` file (or export to Google Calendar with integration?)
