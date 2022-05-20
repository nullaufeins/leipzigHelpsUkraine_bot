#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.thirdparty.api import *;
from src.thirdparty.config import *;
from src.thirdparty.run import *;
from src.thirdparty.system import *;
from src.thirdparty.types import *;
from src.thirdparty.misc import *;
from tests.thirdparty.unit import *;
from tests.thirdparty.integration import *;

from src.core.log import log_dev;
from tests.integration.setup.environment import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CONSTANTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PATH_SESSION = 'tests/.session';
LOOP: Optional[AbstractEventLoop] = None;
START_MESSAGE = 'start-of-test';

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# FIXTURES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@fixture(scope='module', autouse=True)
def test() -> TestCase:
    return TestCase();

@fixture(scope='module', autouse=True)
def debug() -> Callable[..., None]:
    '''
    Fixture for development purposes only.
    Logs to file 'logs/debug.log'.
    '''
    return log_dev;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# FIXTURES for async, telegram client, etc.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# NOTE: !!! Must be called 'event_loop' !!!
@fixture(scope='session', autouse=True)
def event_loop() -> AbstractEventLoop:
    global LOOP;
    if LOOP is None or LOOP.is_closed():
        LOOP = asyncio_new_event_loop();
        asyncio_set_event_loop(loop=LOOP);
    return LOOP;

@fixture(scope='module', autouse=True)
async def environment(event_loop: AbstractEventLoop) -> Environment:
    return Environment();

@fixture(scope='module')
async def client(event_loop: AbstractEventLoop, environment: Environment) -> TelegramClient:
    return await environment.getClient();

@fixture(scope='module')
async def controller(event_loop: AbstractEventLoop, environment: Environment) -> TelegramController:
    return await environment.getController();

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# FIXTURES miscellaneous
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@fixture(scope='function')
async def start_message_id(environment: Environment, client: TelegramClient) -> int:
    sent = await client.send_message(
        chat_id = environment.chat_id,
        text    = f'{START_MESSAGE}\ntimestamp: {datetime.now()}',
    );
    return sent.message_id;
