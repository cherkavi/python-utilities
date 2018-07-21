import sys


def main():
    user_last = None
    query = []
    url = []

    def print_user():
        size = len(query) if len(url)>len(query) else len(url)
        for each_query in query:
            for each_url in url:
                print(user_last + "\t" + each_query + "\t" + each_url)

    for line in sys.stdin:
        input_line = line.split("\t")
        user = input_line[0].strip()
        attributes = input_line[1].split(":")
        attr_name = attributes[0].strip()
        attr_value = attributes[1].strip()
        # print(" >>> " + user + "  " + str(attributes))
        
        if user_last != user:
            print_user()
            user_last = user
            query = []
            url = []
        if attr_name == 'query':
            query.append(attr_value)
        if attr_name == 'url':
            url.append(attr_value)

    if len(query)>0 or len(url)>0:
        print_user()        
        

if __name__ == '__main__':
    main()