#!/usr/bin/env python3

'''
Installing python packages  inside python
'''

import pip  # importing the pakage manage
import os  # Required for calling system commands
import subprocess


def ipy():
    '''Installation function'''

    # Updates pip itself
    subprocess.run(['python', '-m', 'pip', 'install', '--upgrade', 'pip'])

    # Installs moralis
    pip.main(['install', 'moralis'])

# Call above function 

ipy()