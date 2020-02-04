# pip install imapclient
import sys
from imapclient import IMAPClient, FLAGGED, SEEN
from getkey import getkey, keys
from typing import List

if len(sys.argv)<2:
    print("<login> <password>")
    sys.exit(1)
mail_login = sys.argv[1]
mail_password = sys.argv[2]
mail_black_list_words = sys.argv[3]

mail_server = 'imap.ukr.net'
mail_port = 993


def trim_left(text: str, need_to_remove: str) -> str:
    return text[len(need_to_remove):] if text.startswith(need_to_remove) else text


def trim_right(text: str, need_to_remove: str) -> str:
    return text[:-len(need_to_remove)] if text.endswith(need_to_remove) else text

def read_lines(file_name)->[]:
    with open(file_name, "r") as file:
        return list(filter(lambda each_line: len(each_line.strip())>0, [trim_right(each,"\n") for each in file.readlines()]))


def convert_to_lines(data):
    raw_text = str(data[b'BODY[TEXT]'])
    return list(map(lambda each_line: trim_right(each_line.strip(), "=0D"), raw_text.split("\\r\\n")))


def retrive_url(text_lines):
    lines = list(filter(lambda each_line: each_line.find("xing.com/m") >= 0, text_lines))
    if len(lines) > 0:
        candidate=lines[0].strip()
        candidate=trim_right(candidate, "=0D=")
        return trim_left(candidate.strip(), "View message in browser: ")
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


def text_between_delimiters(text_lines: List[str], delimiter: str, delimiter_start: int, delimiter_stop: int, join_delimiter: str = "\n"):
    flag = 0
    return_value = []
    for each_line in text_lines:
        if each_line == delimiter:
            flag = flag + 1
        if delimiter_start<=flag<delimiter_stop:
            return_value.append(trim_right(each_line,"="))
        if flag>delimiter_stop:
            break
    if len(return_value)>0:
        return join_delimiter.join(return_value[1:])
    else:
        return None


def retrieve_title(text_lines: List[str]):
    return text_between_delimiters(text_lines, '----------------------------------------', 2, 3, "")


def retrieve_marker_new_message(text_lines: List[str]) -> bool:
    return text_between_delimiters(text_lines, '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~', 1, 2).find("New message:")>0


def retrieve_text(text_lines: List[str]):
    return text_between_delimiters(text_lines, '----------------------------------------', 3, 4)


def replace_german_chars(text: str) -> str:
    return_value = text.replace("=C3=BC", "ü")
    return_value = return_value.replace("=C3=B6", "ö")    
    return_value = return_value.replace("=C3=9", "ss")    
    return return_value


def any_words_in(message_text: str, criterias: List[str]) -> str:
    search_text = message_text
    for each_word in criterias:
        if search_text.find(each_word) >= 0:
            return each_word
    return None


with IMAPClient(mail_server, port=mail_port, use_uid=True) as server:
    try:
        criteria_black_list = read_lines(mail_black_list_words)
        login_result = server.login(mail_login, mail_password)
        inbox_folder = server.select_folder('INBOX')
        messages = server.search('UNDELETED UNFLAGGED')
        message_amount = len(messages)

        response = server.fetch(messages, ['RFC822', 'BODY[TEXT]'])
        counter = 0
        for msgid, data in response.items():
            text_lines = convert_to_lines(data)
            # print("full text:"+"\n".join(text_lines))
            message_time = retrieve_time(text_lines)
            if message_time is None:
                marker_new_message = retrieve_marker_new_message(text_lines)
                if marker_new_message:
                    print(">>> black.new_message: ")
                    server.delete_messages([msgid, ]) # add "DELETE" flag
                continue
            print("time:", message_time)            
            print("message url:", retrive_url(text_lines))
            message_title = replace_german_chars(retrieve_title(text_lines))
            print("message_title: ", message_title)
            message_text=replace_german_chars(retrieve_text(text_lines))
            # print("offer text", message_text)
            stop_word = any_words_in(message_text, criteria_black_list)
            if stop_word is None:
                stop_word = any_words_in(message_title, criteria_black_list)
            if stop_word is None:
                # server.move(msgid, "work-to-consider")
                server.set_flags([msgid], [SEEN, FLAGGED])
                print(">>> white")
            else:
                server.delete_messages([msgid, ]) # add "DELETE" flag
                print(">>> black: " + stop_word)
            print(" --- --- --- ")
            
        server.expunge() # remove all messages with flag "DELETE"
    except Exception as e:
        print("error:", e.args[0])
