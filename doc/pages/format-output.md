# format-output

## format

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/format-output/format.py) -->
<!-- The below code snippet is automatically added from ../../python/format-output/format.py -->
```py
# format string, print formatted values
a = 10
b = 20
c = "hello"
print("-----")
print( f"{a} {{ curly braces escape example}}  {b}\t{c.upper()}" )
print( "{}   {}\t{}".format(a,b,c) )

print("-----")
print( "  {0:5d}   {1:10d}  \t  {2:10s}".format(a,b,c) )
print( "  {val2:5d}   {val1:10d}  \t  {val3:10s}".format(val1=a,val2=b,val3=c) )

# string formatting
print("-----")
print(f"  {a:_<5}  {c:~^15}  {b:0>10}")


print("-----")
s="hello"
print(">>%20s<<" % (s))
```
<!-- MARKDOWN-AUTO-DOCS:END -->


