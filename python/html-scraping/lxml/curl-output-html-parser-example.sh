for each_page in $(seq 1 105)
do
    echo $each_page
    echo "\n#$each_page#\n" >> strategy-book.txt
    curl --silent "http://loveread.ec/read_book.php?id=66258&p=$each_page" | iconv --from-code WINDOWS-1251 --to-code UTF-8 | python3 curl-output-html-parser.py "/html/body/table/tr[2]/td/table/tr/td[2]/div[3]" >> strategy-book.txt
done
