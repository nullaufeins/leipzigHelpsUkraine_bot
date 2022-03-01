/****************************************************************
 * IMPORTS
 ****************************************************************/

const sprintf = require('sprintf-js').sprintf;
const {
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
    const { command } = command_options;

    // // special treatment if new chat member:
    // if ('new_chat_members' in msg) {
    //     return action_on_new_member(bot, user, msg, options);
    // }

    switch (command) {
        case '/pinned':
            return action_on_pinned(bot, user, msg, command_options);
        case '/hello':
            if (!debug) return;
            return action_on_hello(bot, user, msg, command_options);
        case '/start':
            return action_on_start(bot, user, msg, command_options);
        case '/help':
            return action_on_help(bot, user, msg, command_options);
        default:
            if (('redirect' in command_options) && command_options.redirect) {
                return action_on_redirect(bot, user, msg, command_options);
            }
            return;
    }
}

const action_on_pinned = async (bot, user, msg, command_options) => {
    console.log('Not yet implemented!');
    const chatId = msg.chat.id;
    const lang = msg.from.language_code;
    const { keyword, rights } = command_options;
    if (!user_has_rights(user, rights)) return;

    const responseText = get_translation(lang, keyword);
    const options = get_main_menu_inline(lang);
    const reply = await bot.telegram.sendMessage(chatId, responseText, options);
    const messageId = reply.message_id;
    return bot.telegram.pinChatMessage(chatId, messageId, {disable_notification: true});
}

// const action_on_special = (bot, chatId, lang, username, )
const action_on_new_member = async (bot, user, msg, command_options) => {
    const username = user.username;
    const chatId = msg.chat.id;
    const lang = msg.from.language_code;
    const { keyword, rights } = command_options;
    if (!user_has_rights(user, rights)) return;

    const responseText = sprintf(get_translation(lang, 'welcome-message'), username);
    const options = get_main_menu_inline(lang);
    return bot.telegram.sendMessage(chatId, responseText, options);
}

const action_on_hello = async (bot, user, msg, command_options) => {
    const username = user.username;
    const chatId = msg.chat.id;
    const lang = msg.from.language_code;
    const { keyword, rights } = command_options;
    if (!user_has_rights(user, rights)) return;

    const responseText = sprintf(get_translation(lang, keyword), username);
    const options = get_message_options_basic();
    return bot.telegram.sendMessage(chatId, responseText, options);
}

const action_on_help = async (bot, user, msg, command_options) => {
    const chatId = msg.chat.id;
    const lang = msg.from.language_code;
    const { keyword, rights } = command_options;
    if (!user_has_rights(user, rights)) return;

    const responseText = get_translation(lang, keyword);
    const options = get_main_menu_inline(lang);
    return bot.telegram.sendMessage(chatId, responseText, options);
};

const action_on_start = async (bot, user, msg, command_options) => {
    return action_on_help(bot, user, msg, command_options);
};

const action_on_redirect = async (bot, user, msg, command_options) => {
    const chatId = msg.chat.id;
    const lang = msg.from.language_code;
    const { rights } = command_options;
    if (!user_has_rights(user, rights)) return;

    const { url } = command_options;
    const message = get_translation(lang, 'redirect-message');
    const options = get_message_options_basic();
    const responseText = `${message}: ${url}`;
    return bot.telegram.sendMessage(chatId, responseText, options);
};

 /****************************************************************
  * EXPORTS
  ****************************************************************/

module.exports = {
    universal_action,
};
