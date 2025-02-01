import pytesseract
from PIL import Image

'''
Takes an image path and performs OCR on the image.

:param image_path: The path to the image to perform OCR on.
:return: The text extracted from the image.
'''
def ocr(image_path):
    # Load an image
    image = Image.open(image_path)

    # Perform OCR on the image
    text = pytesseract.image_to_string(image)
    return text
