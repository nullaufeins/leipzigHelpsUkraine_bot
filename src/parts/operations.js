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
    message_too_old,
    remove_message,
    delay_remove_reply,
};
