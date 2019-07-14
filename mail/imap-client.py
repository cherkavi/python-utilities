# pip install imapclient
from imapclient import IMAPClient

mail_login = ''
mail_password = ''
with IMAPClient('imap.ukr.net', port=993, use_uid=True) as server:
	try:
		login_result = server.login(mail_login, mail_password)
		print(login_result)
	except Exception as e:
		print("error:", e.args[0])
		
	