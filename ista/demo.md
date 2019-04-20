# Demo Ista project



## copy zip files
```
cp /home/technik/projects/ista/data/ista-data/*.zip /home/technik/projects/temp/ista/zip-source
```

## execute zip extractor
```
python3 ./soft/zip-opener.py --sourceFolder /home/technik/projects/temp/ista/zip-source --targetFileExtension .behdat --destinationFolder /home/technik/projects/temp/ista/zip-destination --processedFolder /home/technik/projects/temp/ista/zip-processed
```

## execute xml to json converter
```
python3 ./soft/xml2json.py --sourceFolder /home/technik/projects/temp/ista/xml-source --targetFileExtension .behdat --destinationFolder /home/technik/projects/temp/ista/xml-destination --errorFolder /home/technik/projects/temp/ista/xml-error --processedFolder /home/technik/projects/temp/ista/xml-processed
```

## execute file duplication remover
```
python3 ./soft/md5-duplication-remover.py /home/technik/projects/temp/ista/xml-destination
```

## execute json uploader to mongo
```
python3 ./soft/json2mongo.py --sourceFolder /home/technik/projects/temp/ista/json-source --processedFolder /home/technik/projects/temp/ista/json-processed --errorFolder /home/technik/projects/temp/ista/json-error --mongoUrl mongodb://localhost:27017/ --mongoUser vitalii --mongoPassword vitalii --mongoDatabase ista-db --mongoCollection signals
```


---

* Query examples:
```
{ 
"MetaData.Vin7": "BJ97639"
} 
```


* Query examples:
```
{ 
"Data.m005": {$gt: 1000}
} 
```

* Query examples:
```
{ 
$or: [ { "Data.m024": {$lt: 10} }, { "Data.m005": {$gt: 1000} } ]
} 
```

* Query examples:
```
{ 
$and: [ { "Data.m024": {$lt: 10} }, { "Data.m005": {$gt: 1000} } ]
} 
```

