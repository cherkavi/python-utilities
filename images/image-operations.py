from PIL import Image

image = Image.open('1.jpg')
# image.show()
# image.save('1.png')
image.thumbnail((50,50))
image.rotate(90).save('2.jpg')
