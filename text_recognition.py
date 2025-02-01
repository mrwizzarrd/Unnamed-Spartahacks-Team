import cv2
import easyocr

def capture_image():
    # Initialize the camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return None

    # Capture a single frame
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not capture image.")
        return None

    # Release the camera
    cap.release()
    return frame

def recognize_text(image):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image)
    return result

image = capture_image()
if image:
    text = recognize_text(image)
    for (bbox, text, prob) in text:
        print(f"Detected text: {text} (Confidence: {prob:.2f})")

