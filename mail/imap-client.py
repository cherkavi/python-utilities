# pip install imapclient
import sys
from imapclient import IMAPClient

mail_login = sys.argv[1]
mail_password = sys.argv[2]
with IMAPClient('imap.ukr.net', port=993, use_uid=True) as server:
        try:
                login_result = server.login(mail_login, mail_password)
                inboxInfo = server.select_folder('INBOX')
                messages = server.search(['NOT', 'DELETED'])
                response = server.fetch( messages, ['RFC822', 'BODY[TEXT]'] )

                for msgid, data in response.items():                        
                        lines=list(filter(lambda each_line: each_line.find("View message in browser:")>=0, str(data[b'BODY[TEXT]']).split("\\r\\n")))
                        if len(lines)>0:
                                print(lines[0].split(": ")[1].strip())
                        print("---")
        except Exception as e:
                print("error:", e.args[0])
		
	
