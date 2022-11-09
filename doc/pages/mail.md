# mail

## imap client xing remover

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/mail/imap-client-xing-remover.py) -->
<!-- The below code snippet is automatically added from ../../python/mail/imap-client-xing-remover.py -->
```py
# pip install imapclient
import sys
from typing import List, Union

from imapclient import IMAPClient, FLAGGED, SEEN


def trim_left(text: str, need_to_remove: str) -> str:
    if not text:
        return None
    return text[len(need_to_remove):] if text.startswith(need_to_remove) else text


def trim_right(text: str, need_to_remove: str) -> str:
    return text[:-len(need_to_remove)] if text.endswith(need_to_remove) else text


def read_lines_from_blacklist(file_name) -> List[str]:
    with open(file_name, "r") as file:
        return [trim_right(each, "\n") for each in file.readlines() if
                len(each.strip()) > 0 and not each.startswith("#")]


def convert_to_lines(data: dict) -> List[str]:
    raw_text = str(data[b'BODY[TEXT]'])
    return list(map(lambda each_line: trim_right(each_line.strip(), "=0D"), raw_text.split("\\r\\n")))


def retrieve_url(text_lines: List[str]) -> str:
    lines = list(filter(lambda each_line: each_line.find("xing.com/m") >= 0, text_lines))
    if len(lines) > 0:
        candidate = lines[0].strip()
        candidate = trim_right(candidate, "=0D=")
        return trim_left(candidate.strip(), "View message in browser: ")
    else:
        return None


def retrieve_post_source_group(text_lines: List[str]) -> str:
    lines = list(filter(lambda each_line: each_line.find("xing.com/m") >= 0, text_lines))
    if len(lines) > 0:
        candidate = lines[0].strip()
        candidate = trim_right(candidate, "=0D=")
        return trim_left(candidate.strip(), "View message in browser: ")
    else:
        return None


def retrieve_time(text_lines: List[str]) -> str:
    flag = False
    for each_line in text_lines:
        if flag:
            return each_line
        if each_line.endswith("wrote a post:"):
            # need to return next line
            flag = True
    return None


def text_between_delimiters(text_lines: List[str], delimiter: str, delimiter_start: int, delimiter_stop: int,
                            join_delimiter: str = "\n") -> Union[str, None]:
    """ text between delimiters with possibility to count beginning and ending with delimiters """
    flag = 0
    return_value = []
    for each_line in text_lines:
        if each_line.find(delimiter) >= 0:
            flag = flag + 1
        if delimiter_start <= flag < delimiter_stop:
            return_value.append(trim_right(each_line, "="))
        if flag > delimiter_stop:
            break
    if len(return_value) > 0:
        return join_delimiter.join(return_value[1:])
    else:
        return None


def text_between_two_delimiters_inside_line(text_line: str, delimiter_begin: str, delimiter_end: str) -> Union[
    str, None]:
    """ find in line 'delimiter_begin' and 'delimiter_end' """
    index_delimiter_begin = text_line.find(delimiter_begin)
    if index_delimiter_begin >= 0:
        index_delimiter_end = text_line.find(delimiter_end)
        if index_delimiter_end > index_delimiter_begin:
            return text_line[index_delimiter_begin + len(delimiter_begin): index_delimiter_end]
    return None


def retrieve_title(text_lines: List[str]):
    return text_between_delimiters(text_lines, '----------------------------------------', 2, 3, "")


def get_text_after_delimiter(text: str, delimiter: str) -> Union[str, None]:
    delimiter_index = text.find(delimiter)
    return text[delimiter_index + len(delimiter):] if delimiter_index >= 0 else None


def get_text_before_delimiter(text: str, delimiter: str) -> Union[str, None]:
    delimiter_index = text.find(delimiter)
    return text[0:delimiter_index] if delimiter_index >= 0 else None


def retrieve_post_url(text: str) -> str:
    return_value = get_text_after_delimiter(text, "=3D> see more")
    if return_value:
        trimmed_return_value = get_text_before_delimiter(return_value.strip(), "\n").strip()
        return trimmed_return_value if trimmed_return_value else return_value
    else:
        return_value = get_text_after_delimiter(text, "=3D> Go to post")
        return return_value.strip() if return_value else None

def retrieve_marker_new_message(text_lines: List[str]) -> bool:
    text = text_between_delimiters(text_lines, '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~', 1, 2)
    return text and text.find("New message:") > 0


def retrieve_text(text_lines: List[str]) -> str:
    return text_between_delimiters(text_lines, '----------------------------------------', 3, 5)


def replace_german_chars(text: str) -> str:
    # don't replace:
    # =3D>
    return_value = text.replace("=C3=BC", "ü")
    return_value = return_value.replace("=E2=84=96", "№")
    return_value = return_value.replace("=C3=B6", "ö")
    return_value = return_value.replace("=C3=9", "ss")
    return_value = return_value.replace("=C3=A4", "ä")
    return return_value


# return None or string, just a str is not enough, return double type
# another possible option: typing.Optional[str]
def any_words_in(message_text: str, criterias: List[str]) -> Union[str, None]:
    search_text = message_text
    for each_word in criterias:
        if search_text.find(each_word) >= 0:
            return each_word
    return None


def retrieve_message_group_source(message_text_lines: str) -> Union[str, None]:
    """ one of the first lines in the message contains: <title> </title> """
    return trim_left(text_between_two_delimiters_inside_line(message_text_lines, "<title>", "</title>"),
                     "New post in the").replace("=", "").replace("\n", "")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("<login> <password>")
        sys.exit(1)
    mail_login = sys.argv[1]
    mail_password = sys.argv[2]
    mail_black_list_words = sys.argv[3]

    mail_server = 'imap.ukr.net'
    mail_port = 993

    with IMAPClient(mail_server, port=mail_port, use_uid=True) as server:
        try:
            criteria_black_list = read_lines_from_blacklist(mail_black_list_words)
            login_result = server.login(mail_login, mail_password)
            inbox_folder = server.select_folder('INBOX')
            messages = server.search('UNDELETED UNFLAGGED')
            message_amount = len(messages)

            response = server.fetch(messages, ['RFC822', 'BODY[TEXT]'])
            counter = 0
            for msgId, message_data in response.items():
                message_text_lines = convert_to_lines(message_data)
                message_text_one_line = "\n".join(message_text_lines)
                # print("full text:"+"\n".join(text_lines))
                message_time = retrieve_time(message_text_lines)
                if message_time is None:
                    marker_new_message = retrieve_marker_new_message(message_text_lines)
                    if marker_new_message:
                        print(">>> black.new_message: ")
                        server.delete_messages([msgId, ])  # add "DELETE" flag
                    continue
                print("time:", message_time)
                print("group:", retrieve_message_group_source(message_text_one_line))
                print("message_url:", retrieve_url(message_text_lines))
                message_title = replace_german_chars(retrieve_title(message_text_lines))
                print("message_title: ", message_title)
                message_text = replace_german_chars(retrieve_text(message_text_lines))
                print("post_url:", retrieve_post_url(message_text))
                # print("offer text", message_text)
                stop_word = any_words_in(message_text, criteria_black_list)
                if stop_word is None:
                    stop_word = any_words_in(message_title, criteria_black_list)
                if stop_word is None:
                    # server.move(msgid, "work-to-consider")
                    server.set_flags([msgId], [SEEN, FLAGGED])
                    print(">>> white")
                else:
                    server.delete_messages([msgId, ])  # add "DELETE" flag
                    print(">>> black: " + stop_word)
                print(" --- --- --- ")

            server.expunge()  # remove all messages with flag "DELETE"
        except Exception as e:
            print("error:", e.args[0])
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## imap client

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/mail/imap-client.py) -->
<!-- The below code snippet is automatically added from ../../python/mail/imap-client.py -->
```py
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
```
<!-- MARKDOWN-AUTO-DOCS:END -->


