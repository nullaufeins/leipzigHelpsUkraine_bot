#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os;
import sys;

os.chdir(os.path.dirname(__file__));
sys.path.insert(0, os.getcwd());

from src.thirdparty.code import *;
from src.thirdparty.run import *;
from src.thirdparty.types import *;

from src.core.calls import *;
from src.core.log import *;
from src.models.config import *;
from src.setup.config import *;
from src.core.env import *;
from src.app import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MAIN ROUTINE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

async def enter(loop: AbstractEventLoop):
    options = OPTIONS;
    configure_logging(log_level(options));

    log_info('Setup app...');
    secret = Secret();
    app = MyApp(options=OPTIONS, secret=secret);
    app.setup();

    results = await asyncio_gather(*[
        event_listen(loop=loop, app=app),
        event_process_queue(loop=loop, app=app),
    ], return_exceptions = True);

    # # FIXME: does not cancel tasks signal properly:
    # for sig in [SIGINT, SIGTERM]:
    #     loop.add_signal_handler(sig, partial(event_exit_programme, sig, loop, results));

    return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# SUBROUTINES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# # FIXME: does not cancel tasks properly:
# def event_exit_programme(sig: Signals, loop: AbstractEventLoop, pending):
#     log_info(f'Recieved signal {sig}: exit');
#     for task in pending:
#         task.cancel();
#     loop.stop();
#     return;

@to_async(executor=None)
def event_listen(app: MyApp):
    '''
    Routine which listens to user commands and processes them.
    '''
    log_info('Listening to user input...');
    app.start();
    return;

async def event_process_queue(loop: AbstractEventLoop, app: MyApp):
    '''
    Routine which passively works through tasks in database.
    '''
    # NOTE: Not yet implemented
    return;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXECUTION
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    loop = asyncio_new_event_loop();
    loop.run_until_complete(enter(loop));
