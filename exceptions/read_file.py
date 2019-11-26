try:
    f = open('readme.md')
except IOError as e:
    if isinstance(e, Iterable) and len(e) > 0:
        error_message = e[0].message
    else:
        error_message = e.message
    print( 'can't open the file: %s' % (error_message, ) )
else:
    with f:
        print f.readlines()
