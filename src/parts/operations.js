/****************************************************************
 * IMPORTS
 ****************************************************************/

//

/****************************************************************
 * METHODS get aspects
 ****************************************************************/

const get_language_sender_in_message = (msg) => {
    try {
        console.log(`Language from message: ${msg.from.language_code}`)
        return msg.from.language_code;
    } catch(_) {
        return undefined;
    }
}

// true <==> message too old (and should therefore be ignored):
const message_too_old = (msg, t, expiry) => {
    const { date } = msg;
    return (typeof date === 'number') ? (date * 1000 + expiry < t) : true;
};

/****************************************************************
 * METHODS posting
 ****************************************************************/

const send_message = async (bot, text, options, msg) => {
    const chatId = msg.chat.id;
    return bot.telegram
        .sendMessage(chatId, text, options)
        // log error and then carry on:
        .catch((err) => (console.error(err)));
};

const send_message_as_overwrite = async (bot, text, options, msg) => {
    const chatId = msg.chat.id;
    const { message_id } = msg;
    const { reply_markup } = options;
    const { parse_mode } = reply_markup;
    return bot.telegram
        .editMessageText(chatId, message_id, undefined, text, { parse_mode }, undefined, undefined, reply_markup)
        // log error and then carry on:
        .catch((err) => (console.error(err)));
};

const pin_message = async (bot, msg) => {
    const chatId = msg.chat.id;
    const { message_id } = msg;
    return bot.telegram
        .pinChatMessage(chatId, message_id, {disable_notification: true})
        // log error and then carry on:
        .catch((err) => (console.error(err)));
};

const post_and_pin_message = async (bot, text, options, msg) => {
    const reply = await send_message(bot, text, options, msg);
    return pin_message(bot, reply);
}

/****************************************************************
 * METHODS deletion
 ****************************************************************/

const remove_message = async (bot, msg) => {
    const chatId = msg.chat.id;
    const { message_id } = msg;
    bot.telegram
        .deleteMessage(chatId, message_id)
        // log error and then carry on:
        .catch((err) => (console.error(err)));
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
    get_language_sender_in_message,
    message_too_old,
    pin_message,
    send_message,
    send_message_as_overwrite,
    remove_message,
    delay_remove_reply,
};
