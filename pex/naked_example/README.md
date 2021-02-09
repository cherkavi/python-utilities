```sh
# execute file 
python3 .
```

```sh
# execute zip archive
zip example.zip __main__.py
python3 example.zip
```

```sh
# create pex package
cat <(echo '#!/usr/bin/env python3') example.zip > example.pex
chmod +x example.pex
```

```sh
pex --python=python3 -f $PWD requests flask -e __main__.py -o samplepkg.pex
# just an environment
pex --python=python3 flask requests tornado -o samplepkg.pex
```
