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
            this.setup_sidemenu();
        }
        console.log('Connect listeners...');
        this.setup_listeners();
    }

    async setup_sidemenu() {
        const { debug } = this.options;
        for (const _lang of SUPPORTED_LANGUAGES) {
            let commands = COMMANDS
                .filter((options) => ('side_menu' in options))
                .map(({ aspects, side_menu }) => {
                    const { command } = aspects;
                    const { lang, keyword } = side_menu;
                    const description = get_translation(lang || _lang, keyword);
                    return { command, description };
                });
            if (debug) commands.push({ command: `/hello`, description: 'Hello world' });
            await this.bot.telegram.setMyCommands(commands, { language_code: _lang });
        }
    }

    async setup_listeners() {
        /********************************
         * Options for on:
         * - 'callback_query'
         * - 'text'
         * - 'message'
         ********************************/
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
