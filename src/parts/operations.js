/****************************************************************
 * IMPORTS
 ****************************************************************/

const sprintf = require('sprintf-js').sprintf;
const {
    COMMANDS,
    get_command_by_keyword,
    get_command_by_command,
    TRANSLATIONS
} = require.main.require('./parts/parameters.js');

/****************************************************************
 * METHODS
 ****************************************************************/

const remove_message = async (bot, meta) => {
    const chatId = meta.chat.id;
    const message_id = meta.message_id;
    bot.deleteMessage(chatId, message_id);
};

const delay_remove_reply = async (bot, timeout, reply) => {
    // wait for reply, then wait a delayed amount, then delete
    reply.then((meta) => {
        // wait a delayed amount then delete
        setTimeout(() => {
            remove_message(bot, meta);
        }, timeout);
    })
};

/****************************************************************
 * EXPORTS
 ****************************************************************/

module.exports = {
    remove_message,
    delay_remove_reply,
};
