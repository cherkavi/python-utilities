![schema](https://i.postimg.cc/gr9RvCZ6/archimate-enrichment-from-properties.png)

Archimate to SVG export improvement.
Update destination SVG with all links from documentation properties ( also add popup hints to elements).
Documentation property should looks like ( to be depicted on tooltip ):
```
code: https://github.com/cherkavi/
doc: https://my.confluence.com/cherkavi
some additional information that will be skipped
```

execution example
```sh
python3 update-archimate.py source.archimate exported_from_archimate.svg enriched_with_tooltips.svg
```
