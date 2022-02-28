/****************************************************************
 * IMPORTS
 ****************************************************************/

const {
    COMMANDS,
    get_command_by_keyword,
    get_command_by_command,
    SUPPORTED_LANGUAGES,
    TRANSLATIONS
} = require.main.require('./parts/parameters.js');

/****************************************************************
 * METHODS
 ****************************************************************/

// siehe https://github.com/yagop/node-telegram-bot-api/blob/master/doc/api.md#TelegramBot+setMyCommands
const set_bot_commands = async (bot) => {
    for (lang of SUPPORTED_LANGUAGES) {
        const commands = COMMANDS.map(({command, keyword}) => {
            const description = TRANSLATIONS.value(lang, keyword + '-desc');
            return { command, description };
        });
        bot.setMyCommands
        await bot.setMyCommands(commands, { language_code: lang });
    }
}

// Creates inline keyboard categories for the user to select from
const get_category_selection = (lang) => {
    let rows = [];
    for (const {command, keyword, row_index} of COMMANDS) {
        if (rows.length <= row_index) {
            rows.push([]);
        }
        const callback_data = keyword;
        const text = TRANSLATIONS.value(lang, keyword);
        rows[row_index].push({text, callback_data});
    }
    return rows;
};

function remove_message(bot, meta) {
    if ('message' in meta) {
        return remove_message(bot, meta.message);
    }
    const chatId = meta.chat.id;
    const message_id = meta.message_id;
    bot.deleteMessage(chatId, message_id);
};

function delay_remove_reply(bot, timeout, reply) {
    // wait for reply, then wait a delayed amount, then delete
    reply.then((meta) => {
        // wait a delayed amount then delete
        setTimeout(() => {
            remove_message(bot, meta);
        }, timeout);
    })
};

function delay_remove_message_and_reply(bot, timeout, msg, reply) {
    // wait for reply, then wait a delayed amount, then delete
    reply.then((meta) => {
        setTimeout(() => {
            remove_message(bot, msg);
            remove_message(bot, meta);
        }, timeout);
    })
};

// NOTE: chatId = uid for target chat / username of the target channel (in format @channelusername)
function set_bot_listeners(bot, timeout, timeout_menu, debug) {
    // handles user button push:
    bot.on('callback_query', (msg) => {
        // blocks bots:
        if (msg.from.is_bot) return;
        const chatId = msg.message.chat.id;
        const lang = msg.from.language_code;
        const keyword = msg.data;
        const commands = get_command_by_keyword(keyword);
        const { group } = commands[0] || '';
        const message = TRANSLATIONS.value(lang, 'forward-to-channel');
        const responseText = `${message}: ${group}`;
        const options = {};
        if (debug) console.debug(`:callback_query: id=${chatId}; lang=${lang}; keyword=${keyword}, group=${group}.`);
        if (commands.length == 0) return;
        // Trigger response, then delete after delay:
        const reply = bot.sendMessage(chatId, responseText, options);
        delay_remove_reply(bot, timeout, reply);
    });

    // handles inline user query:
    bot.on('message', (msg) => {
        // blocks bots:
        if (msg.from.is_bot) return;
        const chatId = msg.chat.id;
        const lang = msg.from.language_code;
        const command = msg.text;
        if (('new_chat_members' in msg) || ['/start', '/help'].includes(command)) {
            const responseText = TRANSLATIONS.value(lang, 'welcome');
            const options = { reply_markup: { inline_keyboard: get_category_selection(lang) } };
            if (debug) console.debug(`:message->welcome: id=${chatId}; lang=${lang}; command=${command}.`);
            // Trigger response, then delete both response and original inline message after delay:
            const reply = bot.sendMessage(chatId, responseText, options);
            delay_remove_message_and_reply(bot, timeout_menu, msg, reply);
        } else {
            const message = TRANSLATIONS.value(lang, 'forward-to-channel');
            const options = {};
            const commands = get_command_by_command(command);
            const { group } = commands[0] || '';
            const responseText = `${message}: ${group}`;
            if (debug) console.debug(`:message->command: id=${chatId}; lang=${lang}; command=${command}; group=${group}.`);
            if (commands.length == 0) return;
            // Trigger response, then delete both response and original inline message after delay:
            const reply = bot.sendMessage(chatId, responseText, options)
            delay_remove_message_and_reply(bot, timeout, msg, reply);
        }
    });
}

/****************************************************************
 * EXPORTS
 ****************************************************************/

module.exports = {
    set_bot_listeners,
    set_bot_commands,
};
