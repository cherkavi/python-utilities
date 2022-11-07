from hashlib import md5 as md5

def generate_signature(user, password, date):
    user_password_hash = md5("%s/%s" % (user, password)).hexdigest().upper()
    signature = md5("%s%s" % (date, user_password_hash)).hexdigest().upper()
    return signature

print(generate_signature("U20005", "1234", "2016-10-22T22:25:28+03:00"))

