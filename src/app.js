/****************************************************************
 * IMPORTS
 ****************************************************************/

const { Telegraf } = require('telegraf');
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
        // this.bot = new TelegramBot(process.env.token, { polling: true });
        this.bot = new Telegraf(process.env.token, { polling: true });
    }

    async setup() {
        if (this.options.show_side_menu) {
            // siehe https://github.com/yagop/node-telegram-bot-api/blob/master/doc/api.md#TelegramBot+setMyCommands
            console.log('Build side-menu...');
            const { debug } = this.options;
            for (const lang of SUPPORTED_LANGUAGES) {
                let commands = COMMANDS
                    .filter(({side_menu}) => (side_menu))
                    .map(({command, keyword}) => {
                        const description = get_translation(lang, keyword + '-desc') || get_translation(lang, keyword);
                        return { command, description };
                    });
                if (debug) commands.push({
                    'command':      `/hello`,
                    'description': 'Hello world',
                });
                await this.bot.telegram.setMyCommands(commands, { language_code: lang });
            }
        }
        console.log('Connect listeners...');
        this.bot.on('callback_query', async (msg) => {listener_on_callback_query(this.bot, msg, this.options);});
        this.bot.on('message', async (ctx) => {listener_on_message(this.bot, ctx, this.options);});
    }

    async start() {
        this.bot.launch();
        process.once('SIGINT', () => this.bot.stop('SIGINT'));
        process.once('SIGTERM', () => this.bot.stop('SIGTERM'));
    }

    async stop() {
        this.bot.stop();
    }
}

/****************************************************************
 * EXPORTS
 ****************************************************************/

module.exports = {
    MyApp,
};
