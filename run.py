#!/usr/bin/env python
import os
import sys

# set the current directory and add to path
# so the lib are found
os.chdir('src')
sys.path.append(os.getcwd())

# exec main script
import main
