/****************************************************************
 * IMPORTS
 ****************************************************************/

const {
    DEFAULT_LANGUAGE,
} = require('../setup/config.js');
const {
    recognise_language,
} = require('../setup/arguments.js');

/****************************************************************
 * METHODS get aspects
 ****************************************************************/

const getLanguageByPriorityBasic = (lang_cmd, lang_arg) => (recognise_language(lang_cmd || lang_arg || DEFAULT_LANGUAGE));
const getLanguageByPriorityInContext = (context, lang_cmd, lang_arg) => {
    const lang_reply_to = context.getLanguageMessageRepliedTo();
    const lang_caller = context.getLanguageCaller();
    return recognise_language(lang_cmd || lang_arg || lang_reply_to || lang_caller || DEFAULT_LANGUAGE);
};
const getLanguageByPriorityInContextIgnoreCaller = (context, lang_cmd, lang_arg) => {
    const lang_reply_to = context.getLanguageMessageRepliedTo();
    return recognise_language(lang_cmd || lang_arg || lang_reply_to || DEFAULT_LANGUAGE);
};

/****************************************************************
 * METHODS posting
 ****************************************************************/

const send_message = async (bot, msg, text, options) => {
    return bot.telegram
        .sendMessage(msg.getChatId(), text, options)
        // resolve value true indicates that action was taken
        .then((reply) => [true, reply]);
};

const send_message_as_overwrite = async (bot, msg, text, options) => {
    const { reply_markup } = options;
    const { parse_mode } = reply_markup;
    return bot.telegram
        .editMessageText(msg.getChatId(), msg.getMessageId(), undefined, text, { parse_mode }, undefined, undefined, reply_markup)
        // resolve value true indicates that action was taken
        .then((reply) => [true, reply]);
};

const pin_message = async (bot, msg) => {;
    return bot.telegram
        .pinChatMessage(msg.getChatId(), msg.getMessageId(), {disable_notification: true})
        // resolve value true indicates that action was taken
        .then((reply) => [true, reply]);
};

/****************************************************************
 * METHODS deletion
 ****************************************************************/

const remove_message = async (bot, msg) => {
    return bot.telegram
        .deleteMessage(msg.getChatId(), msg.getMessageId())
        // resolve value true indicates that action was taken
        .then((reply) => [true, reply]);
};

/****************************************************************
 * EXPORTS
 ****************************************************************/

module.exports = {
    getLanguageByPriorityBasic,
    getLanguageByPriorityInContext,
    getLanguageByPriorityInContextIgnoreCaller,
    pin_message,
    send_message,
    send_message_as_overwrite,
    remove_message,
};
