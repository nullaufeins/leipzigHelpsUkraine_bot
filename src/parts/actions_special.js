/****************************************************************
 * IMPORTS
 ****************************************************************/

const { sprintf } = require('sprintf-js');
const { try_action1_silently_then_perform_action2 } = require('./../core/utils.js');

const {
    SUPPORTED_LANGUAGES,
    get_translation,
} = require('./../setup/config.js');
const {
    getLanguageByPriorityBasic,
    getLanguageByPriorityInContext,
    getLanguageByPriorityInContextIgnoreCaller,
    pin_message,
    remove_message,
    send_message,
} = require('./../models/operations.js');
const { Message } = require('./../models/message.js');
const {
    get_main_menu_inline,
    get_message_options_basic,
} = require('./menus.js');
const {
    action_empty,
    action_ignore_with_error,
    action_send_message,
} = require('./actions_basic.js');

/****************************************************************
 * METHODS special actions
 ****************************************************************/

const action_on_pin_one_language = async (bot, context, [ lang_arg ], { keyword, lang }, options) => {
    context.track('action:pin');
    lang = getLanguageByPriorityBasic(lang, lang_arg);
    // post menu:
    const responseText = get_translation(lang, keyword);
    const layout_options = get_main_menu_inline(lang);
    // pin menu:
    return try_action1_silently_then_perform_action2(
    async () => {
        context.track('basic-action:delete');
        return remove_message(bot, context.getCallerMessage())
    },
    async() => {
        return send_message(bot, context.getCallerMessage(), responseText, layout_options)
            .then((value) => {
                const [_, reply] = value instanceof Array ? value : [];
                return pin_message(bot, reply);
            });
    });
}

const action_on_pin_all_languages = async (bot, context, { keyword }, options) => {
    context.track('action:pin-all');
    return try_action1_silently_then_perform_action2(
    async () => {
        context.track('basic-action:delete');
        return remove_message(bot, context.getCallerMessage())
    },
    async() => {
        let index = 0;
        let P = action_empty();
        for (const lang of SUPPORTED_LANGUAGES) {
            const responseText = get_translation(lang, keyword);
            const layout_options = get_main_menu_inline(lang);
            if (index == 0) {
                // post then pin 1st menu:
                P = P.then(() => send_message(bot, context.getCallerMessage(), responseText, layout_options))
                    .then((value) => {
                        const [_, reply] = value instanceof Array ? value : [];
                        return pin_message(bot, reply);
                    });
            } else {
                // post all other menus:
                P = P.then(() => send_message(bot, context.getCallerMessage(), responseText, layout_options));
            }
            index += 1;
        }
        return P;
    });
}

const action_on_hello = async (bot, context, [user, user_replied_to], [ lang_arg ], { keyword, lang }, options) => {
    context.track('action:hello');
    // decide whether to reply to caller or replied-to-user (if exists):
    const name = user_replied_to instanceof Message ? user_replied_to.getFirstName() : user.getFirstName();
    lang = getLanguageByPriorityInContext(context, lang, lang_arg);
    // post text:
    const responseText = sprintf(get_translation(lang, keyword), name);
    const layout_options = get_message_options_basic(context.getReplyToMessage());
    return action_send_message(bot, context, responseText, layout_options, options);
}

const action_on_help = async (bot, context, [ lang_arg ], { keyword, lang }, options) => {
    context.track('action:help');
    lang = getLanguageByPriorityInContextIgnoreCaller(context, lang, lang_arg);
    // post menu:
    const responseText = get_translation(lang, keyword);
    const layout_options = get_main_menu_inline(lang, context.getReplyToMessage());
    return action_send_message(bot, context, responseText, layout_options, options);
};

const action_on_redirect = async (bot, context, [ lang_arg ], { group, url }, { keyword, lang }, options) => {
    context.track('action:redirect');
    lang = getLanguageByPriorityInContextIgnoreCaller(context, lang, lang_arg);
    // post text with link:
    const message = get_translation(lang, keyword);
    let responseText = '';
    if (!(group === undefined)) {
        const remark = get_translation(lang, 'redirect-remark');
        responseText = `${message}: ${group}\n\n${remark}`;
    } else if (!(url === undefined)) {
        responseText = `${message}: ${url}`;
    } else {
        // should not occur!
        return action_ignore_with_error(context, sprintf('Command %s missing group/url attribute. Check config.'));
    }
    const layout_options = get_message_options_basic(context.getReplyToMessage());
    return action_send_message(bot, context, responseText, layout_options, options);
};

/****************************************************************
 * EXPORTS
 ****************************************************************/

module.exports = {
    action_on_pin_one_language,
    action_on_pin_all_languages,
    action_on_hello,
    action_on_help,
    action_on_redirect,
};
