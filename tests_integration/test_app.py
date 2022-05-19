#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from thirdparty.api import *;
from thirdparty.code import *;
from thirdparty.tests import *;
from thirdparty.tests_integration import *;
from thirdparty.types import *;

from src.core.utils import *;
from tests_integration.setup.environment import *;
from tests_integration.conftest import START_MESSAGE;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Test strings
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Test strings
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# @mark.usefixtures()
@mark.asyncio
async def test_basic(debug, test: TestCase, environment: Environment, client:TelegramClient, controller: TelegramController, start_message_id: int):
    # simulate basic interaction
    async with controller.collect(
        filters = TelegramFilters.chat(environment.username),
        count    = 1,
        max_wait = 3,
        wait_consecutive = 2,
    ) as ctx:
        sent = await client.send_message(
            chat_id = environment.chat_id,
            text = f'{environment.botname} transport',
        );
    # extract history of messages from start-message:
    history = await client.get_history(chat_id=environment.chat_id, offset_id=start_message_id, limit=10, reverse=True);
    test.assertGreaterEqual(len(history), 2);
    message = history[0];
    test.assertEqual(message.text, START_MESSAGE);
    message = history[1];
    test.assertEqual(message.from_user.username.lstrip('@'), environment.botname.lstrip('@'));
    return;
