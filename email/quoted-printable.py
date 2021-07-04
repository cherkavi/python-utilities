# quoted-printable data
import quopri
str1 = 'äé'
#encoded = quopri.encodestring('äé'.encode('utf-8'))
encoded = quopri.encodestring(str1.encode('utf-8'))
print(encoded)

str2 = '=C3=A4=C3=A9'
decoded_string = quopri.decodestring(str2)
print(decoded_string.decode('utf-8'))
