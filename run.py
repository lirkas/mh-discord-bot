#!/usr/bin/env python
import os
import sys

# set the current directory and add to path
# so the lib are found
os.chdir('src')
sys.path.append(os.getcwd())


import asyncio
import platform

import lib.logutils as logutils
import main


if platform.system()=='Windows':
    # Must be enabled to avoid "event loop already closed" error
    # Can be disabled to improve exiting speed
    # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    pass

try:
    asyncio.run(main.main())
    print('Exiting app')
except KeyboardInterrupt:
    # the client is already closed when this happen
    print('Forcefully Closed')
except:
    logutils.handle_error('../.tests/log', save_last=True)
