# pip install segno


import segno

price_tag = segno.make("my own text")
price_tag.save("out.png", scale=5)


from segno import helpers

# email, geo, mecard, vcard, wifi
qrcode = helpers.make_wifi(ssid='my access point', password='1234567890', security='WPA')
# qrcode.designator
qrcode.save('wifi-access.png', scale=5)


