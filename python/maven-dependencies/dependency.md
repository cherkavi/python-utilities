# build dependencies tree
```
mvn dependency:tree > out.txt
```

# split output to chunks 
```
cat out.txt | python3 ../dependency-splitter.py
rm 001.log
rm 002.log
rm 003.log
```

# find component (commons-lang) into dependency tree
```
cat *.log | python3 ../dependency-finder.py commons-lang
```
