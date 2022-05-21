#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.thirdparty.system import *;
from src.thirdparty.config import *;
from src.thirdparty.types import *;
from src.thirdparty.code import *;
from tests.thirdparty.integration import *;

from src.core.env import *;
from tests.integration.models.client import *;
from tests.integration.models.controller import *;
from models.generated.tests import Credentials as ModelCredentials;
from models.generated.tests import Chat as ModelChat;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'Environment',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CONSTANTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PATH_SECRETS = 'secrets';

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CLASS Environment
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Environment(ModelCredentials, ModelChat, ModelClient, ModelController):
    def __init__(self):
        super().__init__();
        load_dotenv(dotenv_path=os.getcwd());
        env = dotenv_values('.env');
        self.client = None;
        self.controller = None;

        self.token    = get_env_string(env, 'test_token',    '');
        self.api_name = get_env_string(env, 'test_api_name', 'my-test-app');
        self.api_id   = get_env_int(env,    'test_api_id');
        self.api_hash = get_env_string(env, 'test_api_hash');

        self.chat_id  = get_env_int(env,    'test_chat_id');
        self.botname  = get_env_string(env, 'test_botname');
        self.bot_id   = get_env_int(env,    'test_bot_id');
        self.username = get_env_string(env, 'test_username');
        self.user_id  = get_env_int(env,    'test_user_id');
        self.user_phone_number = get_env_string(env, 'test_user_phone');

    async def getClient(self):
        if self.client is None:
            client = TelegramClient(
                session_name = 'tests',
                workdir = PATH_SECRETS,
                api_id = self.api_id,
                api_hash = self.api_hash,
                # bot_token = self.token,
                phone_number = self.user_phone_number,
            );
            await client.start();
            self.session = await client.export_session_string();
            self.client = client;
        return self.client;

    async def getController(self):
        '''
        Controller of user.
        Communicates with peer = bot.
        '''
        if self.controller is None:
            self.controller = TelegramController(
                client = await self.getClient(),
                # peer is user:
                peer = self.user_id,
                raise_no_response = False
            );
        return self.controller;
