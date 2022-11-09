# country-phone

## generate insert

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/country-phone/generate-insert.py) -->
<!-- The below code snippet is automatically added from ../../python/country-phone/generate-insert.py -->
```py
import sys
import csv
# expected first argument - path to file
# generate insert for:
# create table IF NOT EXISTS `phone2country` (
#  `code_2` char(2) NOT NULL PRIMARY KEY,
#  `code_3` char(3) NOT NULL,
#  `name` varchar(64) NOT NULL,
#  `phone_prefix` varchar(10) NOT NULL
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8;


with open(sys.argv[1]) as csv_file:
    reader = csv.reader(csv_file,)
    for row in reader:
        country_name = row[0].strip()
        phone_code = row[1].strip().split(",")[0].replace("-","").replace(" ","")
        code_2 = row[2].split('/')[0].strip()
        code_3 = row[2].split('/')[1].strip()
        print(f"insert into hlm_phone_country(code_2, code_3, country_name, phone_prefix) values ('{code_2}', '{code_3}', '{country_name}', '{phone_code}')")
```
<!-- MARKDOWN-AUTO-DOCS:END -->


