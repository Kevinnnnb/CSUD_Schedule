from PIL import Image
import pytesseract

def ocr_image(image_path):
    img = Image.open(image_path)
    
    text = pytesseract.image_to_string(img)
    
    print("Texte extrait de l'image :\n\n")
    print(text)



image_path = 'Your path to the image file here'

ocr_image(image_path)