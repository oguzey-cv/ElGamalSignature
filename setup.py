from distutils.core import setup, Extension
 
module1 = Extension('hashModule', sources = ['Cypher.c', 'Hash.c', 'main.c'])
 
setup (name = 'hashElGamal',
        version = '1.0',
        description = 'This is a implementation of hash',
        ext_modules = [module1])
