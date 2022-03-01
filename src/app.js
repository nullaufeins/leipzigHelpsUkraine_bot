/****************************************************************
 * IMPORTS
 ****************************************************************/

const TelegramBot = require('node-telegram-bot-api');
const {
    COMMANDS,
    SUPPORTED_LANGUAGES,
    get_translation
} = require.main.require('./src/setup/config.js');
const {
    listener_on_callback_query,
    listener_on_message,
} = require.main.require('./src/parts/listeners.js');

/****************************************************************
 * METHODS
 ****************************************************************/

class MyApp {
    options = {};
    bot = undefined;

    constructor(options) {
        this.options = options;
        this.bot = new TelegramBot(process.env.token, { polling: true });
    }

    async setup() {
        const { debug } = this.options;
        // siehe https://github.com/yagop/node-telegram-bot-api/blob/master/doc/api.md#TelegramBot+setMyCommands
        for (const lang of SUPPORTED_LANGUAGES) {
            let commands = COMMANDS.map(({command, keyword}) => {
                const description = get_translation(lang, keyword + '-desc');
                return { command, description };
            });
            if (debug) commands.push({ 'command': `/hello`, 'description': 'Hello world' });
            await this.bot.setMyCommands(commands, { language_code: lang });
        }
        this.bot.on('callback_query', async (msg) => {listener_on_callback_query(this.bot, msg, this.options);});
        this.bot.on('message', async (msg) => {listener_on_message(this.bot, msg, this.options);});
    }
}

/****************************************************************
 * EXPORTS
 ****************************************************************/

module.exports = {
    MyApp,
};
