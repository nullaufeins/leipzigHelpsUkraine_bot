/****************************************************************
 * IMPORTS
 ****************************************************************/

//

/****************************************************************
 * METHODS
 ****************************************************************/

// true <==> message too old (and should therefore be ignored):
const message_too_old = (msg, t, expiry) => {
    const { date } = msg;
    return (typeof date === 'number') ? (date * 1000 + expiry < t) : true;
};

const send_message = (bot, text, options, msg) => {
    const chatId = msg.chat.id;
    return bot.telegram.sendMessage(chatId, text, options);
};

const send_message_as_overwrite = (bot, text, options, msg) => {
    const chatId = msg.chat.id;
    const { message_id } = msg;
    const { reply_markup } = options;
    const { parse_mode } = reply_markup;
    return bot.telegram.editMessageText(chatId, message_id, undefined, text, { parse_mode }, undefined, undefined, reply_markup);
};

const remove_message = async (bot, msg) => {
    const chatId = msg.chat.id;
    const { message_id } = msg;
    bot.telegram.deleteMessage(chatId, message_id);
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
    message_too_old,
    send_message,
    send_message_as_overwrite,
    remove_message,
    delay_remove_reply,
};
