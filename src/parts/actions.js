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
    pin_message,
    remove_message,
    send_message,
    send_message_as_overwrite,
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

const action_send_message = async (bot, text, options, msg, delete_calls) => {
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
    lang = lang || lang_arg || DEFAULT_LANGUAGE;
    // post menu:
    const responseText = get_translation(lang, keyword);
    const options = get_main_menu_inline(lang);
    // pin menu:
    await remove_message(bot, msg);
    reply = await send_message(bot, responseText, options, msg)
    return pin_message(bot, reply);
}

const action_on_pin_all_languages = async (bot, msg, { keyword }, { debug }) => {
    const n = SUPPORTED_LANGUAGES.length;
    let index = 0;
    for (const lang of SUPPORTED_LANGUAGES) {
        const responseText = get_translation(lang, keyword);
        const options = get_main_menu_inline(lang);
        if (index == 0) {
            // post then pin 1st menu:
            reply = await send_message(bot, responseText, options, msg)
            result = pin_message(bot, reply);
        } else {
            // post all other menus:
            result = send_message(bot, responseText, options, msg);
        }
        // return if last
        if (index == n-1) return result;
        // otherwise await and continue:
        await result;
        index += 1;
    }
    return action_ignore();
}

const action_on_hello = async (bot, user, [ lang_arg ], msg, reply_to_msg, { keyword, lang }, { debug, delete_calls }) => {
    const username = user.user.first_name;
    const lang_caller = msg.from.language_code;
    lang = lang || lang_arg || lang_caller;
    // post text:
    const responseText = sprintf(get_translation(lang, keyword), username);
    const options = get_message_options_basic(reply_to_msg);
    return action_send_message(bot, responseText, options, msg, delete_calls);
}

const action_on_help = async (bot, [ lang_arg ], msg, reply_to_msg, { keyword, lang }, { debug, delete_calls }) => {
    lang = lang || lang_arg || DEFAULT_LANGUAGE;
    // post menu:
    const responseText = get_translation(lang, keyword);
    const options = get_main_menu_inline(lang, reply_to_msg);
    return action_send_message(bot, responseText, options, msg, delete_calls);
};

const action_on_redirect = async (bot, [ lang_arg ], msg, reply_to_msg, { redirect }, { keyword, lang }, { debug, delete_calls }) => {
    lang = lang || lang_arg || DEFAULT_LANGUAGE;
    // post text with link:
    const message = get_translation(lang, keyword);
    const responseText = `${message}: ${redirect}`;
    const options = get_message_options_basic(reply_to_msg);
    return action_send_message(bot, responseText, options, msg, delete_calls);
};

/****************************************************************
 * EXPORTS
 ****************************************************************/

module.exports = {
    universal_action,
    action_ignore,
    action_delete_and_ignore,
};
