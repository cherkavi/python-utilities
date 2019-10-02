# pip install imapclient
import sys
from imapclient import IMAPClient

mail_login = sys.argv[1]
mail_password = sys.argv[2]

mail_server = 'imap.ukr.net'
mail_port = 993

def process_message(text):
        lines=list(filter(lambda each_line: each_line.find("xing.com/m")>=0, text.split("\\r\\n")))
        if len(lines)>0:
                return lines[1]
        else:
                return None


with IMAPClient(mail_server, port=mail_port, use_uid=True) as server:
        try:
                login_result = server.login(mail_login, mail_password)
                server.select_folder('INBOX')
                # 'NOT DELETED', '1:50'
                messages = server.search(['NOT', 'DELETED'])
                response = server.fetch( messages, ['RFC822', 'BODY[TEXT]'] )

                for msgid, data in response.items():
                        text = str(data[b'BODY[TEXT]'])
                        print(process_message(text))
                        print("---")
        except Exception as e:
                print("error:", e.args[0])
		
	
