## pex installation
```sh
apt install pex
```

## pex build
```sh
rm -rf ./target
rm -rf ./naked_example/__pycache__
mkdir -p ./target

# build PEX package
pex -v --disable-cache -r requirements.txt -o target/naked_example.pex
pex -v --disable-cache -r requirements.txt -o target/naked_example.pex --python=python2

# or full package list
pex $(pip freeze) -o target/naked_example.pex --python=python3 
```

## pex execution
```sh
./target/naked_example.pex naked_example/main.py simple.json
```

-------------------------------------------------

## execute folder with magic file
```sh
python3 ./magic_name
```
## build package manually
```sh
# execute zip archive
rm -rf ./magic_name/__pycache__
cd magic_name
zip example.zip ./__main__.py
python3 example.zip
```
```sh
# create pex package
cat <(echo '#!/usr/bin/env python3') example.zip > example.pex
chmod +x example.pex
./example.pex
```


---------------------------------------
## examples of building PEX 
```sh
# build package 
pex -f $PWD requests flask -e __main__.py -o samplepkg.pex
# build package for specific python environment 
pex --python=python3  -f $PWD requests flask -e __main__.py -o samplepkg.pex
# just an environment
pex --python=python3 flask requests tornado -o samplepkg.pex
```

---------------------------------------
## start inside docker container 
run container and map current folder 
```sh
docker run --volume $(pwd):/host_folder --rm -it alpine /bin/sh
docker run --entrypoint="" --volume $(pwd):/host_folder --rm -it maprtech/pacc:6.1.0_6.0.0_ubuntu16 /bin/sh
```
inside the container:
```sh
cd /host_folder
./target/naked_example.pex naked_example/main.py simple.json
```