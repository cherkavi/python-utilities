import smtplib
from email.mime.text import MIMEText

#with open(textfile, 'rb') as fp:
    # Create a text/plain message
#    msg = MIMEText(fp.read())

msg = MIMEText("simple text message ")
msg['Subject'] = 'just a subject'
msg['From'] = "vitali.cherkashyn@localhost.com"
msg['To'] = "vitali.cherkashyn@vodafone.com"


# Send the message via our own SMTP server, but don't include the
# envelope header.
s = smtplib.SMTP('localhost:2525')
s.sendmail("vitali.cherkashyn@localhost.com", ["vitali.cherkashyn@vodafone.com"], msg.as_string())
s.quit()


import yagmail
yag = yagmail.SMTP(user=mail_login, password=mail_password)
yag.send('somename@somewhere.com', subject = None, contents = 'Hello')

