#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os;
import sys;

os.chdir(os.path.dirname(__file__));
sys.path.insert(0, os.getcwd());

from src.thirdparty.run import *;

from src.core.log import *;
from src.models.config import *;
from src.setup.config import *;
from src.setup.env import *;
from src.app import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MAIN
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

async def enter(event_loop: asyncio.AbstractEventLoop):
    options = OPTIONS;
    configure_logging(log_level(options));

    log_info('Setup app...');
    secret = Secret();
    app = MyApp(options=OPTIONS, secret=secret);
    app.setup();
    await asyncio.gather(
        event_listen(event_loop, app=app),
        event_process_queue(event_loop, app=app),
        return_exceptions=True,
    );
    return;

async def event_listen(event_loop: asyncio.AbstractEventLoop, app: MyApp):
    log_info('Listening to user input...');
    await app.start();
    return;

async def event_process_queue(event_loop: asyncio.AbstractEventLoop, app: MyApp):
    # NOTE: Not yet implemented
    return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXECUTION
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    event_loop = asyncio.new_event_loop();
    event_loop.run_until_complete(enter(event_loop));
