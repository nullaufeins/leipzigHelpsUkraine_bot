/****************************************************************
 * IMPORTS
 ****************************************************************/

const sprintf = require('sprintf-js').sprintf;
const {
    get_command_by_keyword,
    get_command_by_command,
    get_translation,
} = require.main.require('./setup/config.js');
const {
    remove_message,
    delay_remove_reply,
} = require.main.require('./application/operations.js');
const {
    get_main_menu,
    get_message_options_basic,
} = require.main.require('./application/menus.js');

/****************************************************************
 * METHODS - LISTENERS
 ****************************************************************/

// NOTE: chatId = uid for target chat / username of the target channel (in format @channelusername)
// handles user button push:
const listener_on_callback_query = async (bot, msg, {debug, timeout}) => {
    if (msg.from.is_bot) return; // <- blocks bots.
    const chatId = msg.message.chat.id;
    const lang = msg.from.language_code;
    const keyword = (msg.data || '').trim();;
    const commands = get_command_by_keyword(keyword);
    const { group } = commands[0] || '';
    const message = get_translation(lang, 'redirect-message');
    const responseText = `${message}: ${group}`;
    const options = get_message_options_basic();
    if (debug) console.debug(`:callback_query: id=${chatId}; lang=${lang}; keyword=${keyword}, group=${group}.`);
    if (commands.length == 0) return;

    // Trigger response, then delete after delay:
    const reply = bot.sendMessage(chatId, responseText, options);
    delay_remove_reply(bot, timeout, reply);
};

// handles inline user query:
const listener_on_message = async (bot, msg, {debug, timeout, timeout_menu}) => {
    if (msg.from.is_bot) return; // <- blocks bots.
    const username = msg.from.username;
    const chatId = msg.chat.id;
    const lang = msg.from.language_code;
    const command = (msg.text || '').trim();

    // special treatment if new chat member:
    if ('new_chat_members' in msg) {
        const responseText = sprintf(get_translation(lang, 'welcome-message'), username);
        const options = get_main_menu(lang);

        // Trigger response, then delete response after delay:
        const reply = bot.sendMessage(chatId, responseText, options);
        delay_remove_reply(bot, timeout_menu, reply);
        return;
    }

    // force ignore, if input not obviously recognisable as a command:
    if (!command.startsWith('/')) {
        return;
    }

    const commands = get_command_by_command(command);
    // Response to `/hello` - command only available in debug mode:
    if (debug && (command == '/hello')) {
        const responseText = sprintf(get_translation(lang, 'hello-world'), username);
        const options = get_message_options_basic();

        // Delete message, trigger response, then delete response after delay:
        remove_message(bot, msg);
        const reply = bot.sendMessage(chatId, responseText, options);
        delay_remove_reply(bot, timeout, reply);
    // Response to `/start`
    } else if (command == '/start') {
        const responseText = get_translation(lang, 'start-message');
        const options = get_main_menu(lang);

        // Trigger response, then delete response after delay:
        const reply = bot.sendMessage(chatId, responseText, options);
        delay_remove_reply(bot, timeout_menu, reply);
    // Response to `/help`
    } else if (command == '/help') {
        const responseText = get_translation(lang, 'help-message');
        const options = get_main_menu(lang);

        // Delete message, trigger response, then delete response after delay:
        remove_message(bot, msg);
        const reply = bot.sendMessage(chatId, responseText, options);
        delay_remove_reply(bot, timeout_menu, reply);
    // Response to command from list:
    } else if (commands.length > 0) {
        const message = get_translation(lang, 'redirect-message');
        const options = get_message_options_basic();
        const { group } = commands[0] || '';
        const responseText = `${message}: ${group}`;

        // Delete message, trigger response, then delete response after delay:
        remove_message(bot, msg);
        const reply = bot.sendMessage(chatId, responseText, options);
        delay_remove_reply(bot, timeout, reply);
    }

    // otherwise ignore the message and remain passive!
}

/****************************************************************
 * EXPORTS
 ****************************************************************/

module.exports = {
    listener_on_callback_query,
    listener_on_message,
};
