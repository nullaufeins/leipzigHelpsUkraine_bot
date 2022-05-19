#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from thirdparty.api import *;
from thirdparty.code import *;

from src.core.env import *;
from src.core.log import *;
from src.models.config import *;
from src.models.telegram import *;
from src.behaviour.listeners import *;
from src.behaviour.recognition import *;
from src.setup.config import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'MyApp',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CLASS MyApp
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MyApp():
    '''
    A customised telegram bot application with limited interaction.
    See https://github.com/eternnoir/pyTelegramBotAPI for details on the API.
    '''
    options: AppOptions;
    bot: MyBot;

    def __init__(
        self,
        options: AppOptions,
        secret: Secret,
    ):
        self.options = options;
        self.bot = MyBot(secret.token, parse_mode=PARSE_MODE.NONE.value);
        return;

    def setup(self):
        if self.options.show_side_menu:
            log_info('Build side-menu...');
            self.setup_sidemenu();
        log_info('Connect listeners...');
        self.setup_listeners();
        return;

    def setup_sidemenu(self):
        commands_with_side_menu = list(filter(lambda command: not(command.side_menu is None), COMMANDS));
        for lang in SUPPORTED_LANGUAGES:
            commands = [
                TgBotCommand(
                    command     = command.aspects.command,
                    # NOTE: description must be at least 3 characters long!
                    description = get_translation(
                        keyword = command.side_menu.keyword,
                        lang    = command.side_menu.lang or lang,
                    ),
                )
                for command in commands_with_side_menu
            ];
            if self.options.debug:
                commands.append({ 'command': r'/hello', 'description': 'Hello world' });
            self.bot.set_my_commands(
                commands = commands,
                language_code=lang
            );
        return;

    def setup_listeners(self):
        '''
        Sets listeners for commands on text.
        '''
        if self.options.listen_to_text:
            @self.bot.message_handler(content_types=['text'])
            @log_listener(bot=self.bot, app_options=self.options)
            def listener(bot: MyBot, context: CallContext, app_options=self.options):
                return listener_on_text(bot=bot, context=context, app_options=app_options);
        else:
            @self.bot.message_handler(content_types=['text'])
            @log_listener(bot=self.bot, app_options=self.options)
            def listener(bot: MyBot, context: CallContext, app_options=self.options):
                return listener_on_message(bot=bot, context=context, app_options=app_options);
        return;

    def start(self):
        self.bot.polling();
        return;

    def __del__(self):
        # await self.bot.stop_poll(); # NOTE: this only works for specific chats.
        self.bot.stop_bot(); # NOTE: only for non-synch version.
        del self.bot;
        return;
