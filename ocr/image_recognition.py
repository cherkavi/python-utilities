# tesseract ocr image recognition

import cv2
import numpy as np
import pytesseract
from PIL import Image

image_path=~/Screenshot.png
im= cv2.imread(image_path,cv2.IMREAD_GRAYSCALE)
cv2.imshow('Gray', im)
cv2.imwrite(image_path, im)
print(pytesseract.image_to_string(Image.open(image_path)))

