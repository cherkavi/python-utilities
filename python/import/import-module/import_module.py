# import whole module ( point out to __init__.py)
import some_module as ext_module

if __name__=='__main__':
    ext_module.custom_echo()
    ext_module.custom_print()