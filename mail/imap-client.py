# pip install imapclient
import sys
from imapclient import IMAPClient, FLAGGED, SEEN
from getkey import getkey, keys

if len(sys.argv)<2:
    print("<login> <password>")
    sys.exit(1)
mail_login = sys.argv[1]
mail_password = sys.argv[2]

mail_server = 'imap.ukr.net'
mail_port = 993


def retrive_url(text_lines):
    lines = list(filter(lambda each_line: each_line.find("xing.com/m") >= 0, text_lines))
    if len(lines) > 0:
        return lines[1]
    else:
        return None


def retrieve_time(text_lines):
    flag = False
    for each_line in text_lines:
        if flag:
            return each_line
        if each_line.endswith("wrote a post:"):
            flag = True
    return None


def retrieve_title(text_lines):
    delimiter = '----------------------------------------'
    flag = False
    return_value = []
    for each_line in text_lines:
        if flag:
            return_value.append(each_line)
        if each_line.startswith(delimiter):
            if flag:
                break
            else:
                flag = True
    return " ".join(return_value[:-1])


def convert_to_lines():
    raw_text = str(data[b'BODY[TEXT]'])
    return raw_text.split("\\r\\n")


with IMAPClient(mail_server, port=mail_port, use_uid=True) as server:
    try:
        login_result = server.login(mail_login, mail_password)
        # print(login_result) # b'LOGIN completed'
        print("--- capabilities ---")        
        print(server.capabilities())
        print("--------------------")
        inbox_folder = server.select_folder('INBOX')
        print("---- inbox ---")
        print(inbox_folder)
        print("---- ----- ---")
        # 'ALL', 'BEFORE date', 'ON date', 'SINCE date', 'SUBJECT string', 'BODY string', 'TEXT string', 'FROM string','TO string','CC string','BCC string', 'SEEN', 'UNSEEN', 'ANSWERED', 'UNANSWERED', 'DELETED','UNDELETED','DRAFT','UNDRAFT', 'FLAGGED', 'UNFLAGGED', 'LARGER N', 'SMALLER N', 'NOT search-key', 'OR search-key1 search-key2'.
        # messages = server.search(['NOT', 'DELETED', '1:2'])
        # messages = server.search(['UNDELETED', '1:2'])
        messages = server.search('UNDELETED UNFLAGGED')
        message_amount = len(messages)

        # response = server.fetch(messages[:10], ['RFC822', 'BODY[TEXT]'])
        response = server.fetch(messages[:10], ['RFC822', 'BODY[TEXT]'])
        counter = 0
        for msgid, data in response.items():
            text_lines = convert_to_lines()
            # print(msgid)
            print(retrive_url(text_lines))
            print(retrieve_time(text_lines))
            print(retrieve_title(text_lines))
            counter += 1
            print(f"??? {counter}/{message_amount}")
            user_choice = getkey()
            if user_choice == keys.DELETE:
                server.delete_messages([msgid, ]) # add "DELETE" flag
                continue
            if user_choice == keys.ESCAPE:
                break
            server.set_flags([msgid], [SEEN, FLAGGED])
            # server.move(msgid, "work-to-consider")
        server.expunge() # remove all messages with flag "DELETE"
    except Exception as e:
        print("error:", e.args[0])
