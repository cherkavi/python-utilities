import sys

def increase_word(word_dict, next_word):
    if len(next_word)==0:
        return
    if next_word in word_dict:
        word_dict[next_word] = word_dict[next_word]+1
    else:
        word_dict[next_word] = 1


def map_line(string_with_words, words):
    for each_word in string_with_words.split(" "):
        increase_word(words, each_word.strip())

def main():
    words = {}
    for each_line in sys.stdin:
        map_line(each_line, words)
    for key,value in words.items():
        print(key+"\t"+str(value))


if __name__ == '__main__':
    main()