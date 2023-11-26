# pip install python-barcode Pillow

import barcode
from barcode.writer import ImageWriter
from PIL import Image
import sys

def generate_barcode(text, filename):
    # Create a barcode object
    code = barcode.get('code128', text, writer=ImageWriter())

    # Save the barcode as an image
    code.save(filename)

    # Open the generated image and resize it if needed
    # img = Image.open(filename)
    # img = img.resize((300, 150))  # Adjust the size as needed
    # img.save(filename)

if __name__ == "__main__":
    generate_barcode(sys.argv[1], 'out.png')
    print("barcode generated in out.png")
