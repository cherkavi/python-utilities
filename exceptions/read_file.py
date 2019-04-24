try:
    f = open('readme.md')
except IOError as e:
    print( 'can't open the file: %s' % (e.args[0], ) )
else:
    with f:
        print f.readlines()
