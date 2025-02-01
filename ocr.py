import pytesseract
from PIL import Image

def ocr(image_path):
    # Load an image
    image = Image.open(image_path)

    # Perform OCR on the image
    text = pytesseract.image_to_string(image)
    return text
