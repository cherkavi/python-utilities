in/env python

# pip install argcomplete
# .bashrc: 
# ```eval "$(register-python-argcomplete autocomplete-example.py)"```
import argparse
from argcomplete.completers import EnvironCompleter

def main(**args):
    pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('operation', choices=['create', 'delete']).completer = ChoicesCompleter(('create', 'delete'))
    parser.add_argument('--timeout', choices=['5', '10', '15'], ).completer = EnvironCompleter
    argcomplete.autocomplete()

    args = parser.parse_args()
    main(**vars(args))
