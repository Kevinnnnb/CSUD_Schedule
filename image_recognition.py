import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract' # Replace with the path to your Tesseract executable (execute this to get the path : 'which tesseract')

def ocr_image(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    print(text)

# Example usage
image_path = '' #Replace with your image file path
ocr_image(image_path)