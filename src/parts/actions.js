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
    get_main_menu_inline,
    get_message_options_basic,
} = require.main.require('./src/parts/menus.js');
const {
    get_user_from_context,
    user_has_rights,
} = require.main.require('./src/parts/users.js');

/****************************************************************
 * METHODS - ACTIONS
 ****************************************************************/

const universal_action = async (bot, ctx, command_options, { debug }) => {
    const user = await get_user_from_context(bot, ctx);
    const msg = ctx.update.message;
    const { aspects, text } = command_options;
    const { command } = aspects;

    /*
    NOTE: Not currently implemented.

    // special treatment if new chat member:
    if ('new_chat_members' in msg) {
        ...
    }
    */

    if ('redirect' in aspects) {
        return action_on_redirect(bot, user, msg, aspects, text);
    }

    switch (command) {
        case '/pin_all':
            return action_on_pin_all_languages(bot, user, msg, aspects, text);
        case command.match(/^\/pin(?:|_(.*))$/)?.input:
            return action_on_pin_one_language(bot, user, msg, aspects, text);
        case '/hello':
            if (!debug) return;
            return action_on_hello(bot, user, msg, aspects, text);
        case '/help':
            return action_on_help(bot, user, msg, aspects, text);
        default:
            return;
    }
}

const action_on_pin_one_language = async (bot, user, msg, { rights }, { keyword, lang }) => {
    if (!user_has_rights(user, rights)) return;
    const chatId = msg.chat.id;
    lang = lang || DEFAULT_LANGUAGE;
    // post menu:
    const responseText = get_translation(lang, keyword);
    const options = get_main_menu_inline(lang);
    const reply = await bot.telegram.sendMessage(chatId, responseText, options);
    // pin menu:
    const messageId = reply.message_id;
    return bot.telegram.pinChatMessage(chatId, messageId, {disable_notification: true});
}

const action_on_pin_all_languages = async (bot, user, msg, { rights }, { keyword }) => {
    if (!user_has_rights(user, rights)) return;
    const chatId = msg.chat.id;
    let index = 0;
    let messageId = -1;
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

const action_on_hello = async (bot, user, msg, { rights }, { keyword, lang }) => {
    if (!user_has_rights(user, rights)) return;
    const username = user.username;
    const chatId = msg.chat.id;
    const lang_caller = msg.from.language_code;
    lang = lang || lang_caller;
    // post text:
    const responseText = sprintf(get_translation(lang, keyword), username);
    const options = get_message_options_basic();
    return bot.telegram.sendMessage(chatId, responseText, options);
}

const action_on_help = async (bot, user, msg, { rights }, { keyword, lang }) => {
    if (!user_has_rights(user, rights)) return;
    const chatId = msg.chat.id;
    const lang_caller = msg.from.language_code;
    lang = lang || lang_caller;
    // post menu:
    const responseText = get_translation(lang, keyword);
    const options = get_main_menu_inline(lang);
    return bot.telegram.sendMessage(chatId, responseText, options);
};

const action_on_redirect = async (bot, user, msg, { rights, redirect }, { keyword, lang }) => {
    if (!user_has_rights(user, rights)) return;
    const chatId = msg.chat.id;
    const lang_caller = msg.from.language_code;
    lang = lang || lang_caller;
    // post text with link:
    const message = get_translation(lang, keyword);
    const responseText = `${message}: ${redirect}`;
    const options = get_message_options_basic();
    return bot.telegram.sendMessage(chatId, responseText, options);
};

/****************************************************************
 * EXPORTS
 ****************************************************************/

module.exports = {
    universal_action,
};
