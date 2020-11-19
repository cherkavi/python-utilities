[source of data](https://public.opendatasoft.com/explore/dataset/us-zip-code-latitude-and-longitude/export/)
```sh
wget https://public.opendatasoft.com/explore/dataset/us-zip-code-latitude-and-longitude/download/?format=csv&timezone=Europe/Berlin&lang=en&use_labels_for_header=true&csv_separator=%3B
```


```sql
create table IF NOT EXISTS `zip_code` (
  `zip_code_id` INT UNSIGNED PRIMARY KEY,  
  `zip` VARCHAR(16) NOT NULL,
  `city` VARCHAR(48) NOT NULL,
  `state_code` VARCHAR(8) NOT NULL,
  `country_code` VARCHAR(8) NOT NULL,
  `latitude` DOUBLE NOT NULL,
  `longitude` DOUBLE NOT NULL,
  `timezone` INT,
  `daylight_saving` SMALLINT 
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

```


```sh
cat ~/Downloads/us-zip-code-latitude-and-longitude.csv | python3 csv-to-sql.py > out.sql
```
