process.env.NTBA_FIX_319 = 1;
/****************************************************************
 * IMPORTS
 ****************************************************************/

const Config = require('dotenv').config();
const TelegramBot = require('node-telegram-bot-api');

const { OPTIONS } = require.main.require('./settings/config.js');
const { set_bot_listeners } = require('./parts/listeners.js');
const { set_bot_commands } = require('./parts/listeners.js');

/****************************************************************
 * METHODS
 ****************************************************************/

function main () {
    const debug = OPTIONS['debug'] || false;
    const timeout = OPTIONS['timeout'] || 10*1000;
    const timeout_menu = OPTIONS['timeout-menu'] || 60*1000;
    const bot = new TelegramBot(process.env.token, { polling: true });
    set_bot_commands(bot);
    set_bot_listeners(bot, timeout, timeout_menu, debug);
}

/****************************************************************
 * EXECUTION
 ****************************************************************/

main();
