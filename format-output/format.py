# format string, print formatted values
a = 10
b = 20
c = "hello"
print( f"{a} {{escape example}}  {b}\t{c.upper()}" )
print( "{}   {}\t{}".format(a,b,c) )

print( "{0:5d}   {1:10d}\t{2:10s}".format(a,b,c) )
print( "{val2:5d}   {val1:10d}\t{val3:10s}".format(val1=a,val2=b,val3=c) )