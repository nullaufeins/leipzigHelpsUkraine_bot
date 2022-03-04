/****************************************************************
 * IMPORTS
 ****************************************************************/

const sprintf = require('sprintf-js').sprintf;
const {
    DEFAULT_LANGUAGE,
    SUPPORTED_LANGUAGES,
    get_translation,
} = require.main.require('./src/setup/config.js');
const {
    send_message,
    send_message_as_overwrite,
    remove_message,
} = require.main.require('./src/parts/operations.js');
const {
    get_main_menu_inline,
    get_message_options_basic,
} = require.main.require('./src/parts/menus.js');
const {
    get_user_from_context,
    user_has_rights,
} = require.main.require('./src/parts/users.js');

/****************************************************************
 * METHODS universal action
 ****************************************************************/

const universal_action = async (bot, ctx, command_options, arguments, { debug, delete_calls }) => {
    const user = await get_user_from_context(bot, ctx);
    const msg = ctx.update.message;
    const { reply_to_message } = msg;
    const { aspects, text } = command_options;
    const { command, rights } = aspects;

    /*
    NOTE: Not currently implemented.

    // special treatment if new chat member:
    if ('new_chat_members' in msg) {
        ...
    }
    */

    if (!user_has_rights(user, rights)) return;

    if ('redirect' in aspects) {
        return action_on_redirect(bot, arguments, msg, reply_to_message, aspects, text, { debug, delete_calls });
    }

    switch (command) {
        case command.match(/^\/pin(?:|_(.*))$/)?.input:
            const [ flag ] = arguments;
            if (flag === 'all') {
                return action_on_pin_all_languages(bot, msg, text, { debug, delete_calls });
            }
            return action_on_pin_one_language(bot, arguments, msg, text, { debug, delete_calls });
        case '/hello':
            if (debug) {
                const user = await get_user_from_context(bot, ctx);
                return action_on_hello(bot, user, arguments, msg, reply_to_message, text, { debug, delete_calls });
            }
        case '/help':
            return action_on_help(bot, arguments, msg, reply_to_message, text, { debug, delete_calls });
        default:
            return action_delete_and_ignore();
    }
};

/****************************************************************
 * METHODS basic and generic actions
 ****************************************************************/

const action_ignore = async () => {
    return;
};

const action_delete_and_ignore = async (bot, msg) => {
    return remove_message(bot, msg);
};

const action_send_message = async (bot, text, options, msg, as_reply, delete_calls) => {
    if (delete_calls) {
        await remove_message(bot, msg);
        return send_message(bot, text, options, msg);
    } else {
        return send_message_as_overwrite(bot, text, options, msg);
    }
};

/****************************************************************
 * METHODS special actions
 ****************************************************************/

const action_on_pin_one_language = async (bot, [ lang_arg ], msg, { keyword, lang }, { debug }) => {
    const chatId = msg.chat.id;
    lang = lang || lang_arg || DEFAULT_LANGUAGE;
    // post menu:
    const responseText = get_translation(lang, keyword);
    const options = get_main_menu_inline(lang);
    const reply = await bot.telegram.sendMessage(chatId, responseText, options);
    // pin menu:
    const messageId = reply.message_id;
    await remove_message(bot, msg);
    return bot.telegram.pinChatMessage(chatId, messageId, {disable_notification: true}, true);
}

const action_on_pin_all_languages = async (bot, msg, { keyword }, { debug }) => {
    const chatId = msg.chat.id;
    let index = 0;
    let messageId = -1;
    await remove_message(bot, msg);
    for (const lang of SUPPORTED_LANGUAGES) {
        // post menu:
        const responseText = get_translation(lang, keyword);
        const options = get_main_menu_inline(lang);
        const reply = await bot.telegram.sendMessage(chatId, responseText, options);
        if (index == 0) messageId = reply.message_id;
        index += 1;
    }
    // pin 1st menu:
    if (messageId >= 0) {
        return bot.telegram.pinChatMessage(chatId, messageId, {disable_notification: true});
    }
}

const action_on_hello = async (bot, user, [ lang_arg ], msg, reply_to_msg, { keyword, lang }, { debug, delete_calls }) => {
    const username = user.user.first_name;
    const lang_caller = msg.from.language_code;
    lang = lang || lang_arg || lang_caller;
    // post text:
    const responseText = sprintf(get_translation(lang, keyword), username);
    const options = get_message_options_basic(reply_to_msg);
    return action_send_message(bot, responseText, options, msg, !(reply_to_msg === undefined), delete_calls);
}

const action_on_help = async (bot, [ lang_arg ], msg, reply_to_msg, { keyword, lang }, { debug, delete_calls }) => {
    lang = lang || lang_arg || DEFAULT_LANGUAGE;
    // post menu:
    const responseText = get_translation(lang, keyword);
    const options = get_main_menu_inline(lang, reply_to_msg);
    return action_send_message(bot, responseText, options, msg, !(reply_to_msg === undefined), delete_calls);
};

const action_on_redirect = async (bot, [ lang_arg ], msg, reply_to_msg, { redirect }, { keyword, lang }, { debug, delete_calls }) => {
    lang = lang || lang_arg || DEFAULT_LANGUAGE;
    // post text with link:
    const message = get_translation(lang, keyword);
    const responseText = `${message}: ${redirect}`;
    const options = get_message_options_basic(reply_to_msg);
    return action_send_message(bot, responseText, options, msg, !(reply_to_msg === undefined), delete_calls);
};

/****************************************************************
 * EXPORTS
 ****************************************************************/

module.exports = {
    universal_action,
    action_ignore,
    action_delete_and_ignore,
};
