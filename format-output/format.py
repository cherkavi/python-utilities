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

# f-string conversation character
class Example:
    def __str__(self) -> str:
        return "show str"
    def __repr__(self) -> str:
        return "show repr юникод"  

print(f"{Example()!r}") # __repr__
print(f"{Example()!s}") # __str__
print(f"{Example()!a}") #  like ascii (escapes unicode)
