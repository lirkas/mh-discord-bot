#!/usr/bin/env python
import os
import sys
import setproctitle

# set the current directory and add to path
# so the lib are found
os.chdir('src')
sys.path.append(os.getcwd())

# sets the process name of this running instance
setproctitle.setproctitle('py-mhbot-7940')

# exec main script
import main
