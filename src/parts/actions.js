/****************************************************************
 * IMPORTS
 ****************************************************************/

const {
    action_delete_and_ignore,
} = require('./actions_basic.js');
const {
    action_on_pin_one_language,
    action_on_pin_all_languages,
    action_on_hello,
    action_on_help,
    action_on_redirect,
} = require('./actions_special.js');

/****************************************************************
 * METHODS universal action
 ****************************************************************/

const universal_action = async (bot, context, command_options, arguments, options) => {
    const { aspects, text } = command_options;
    const { command, rights, redirect } = aspects;
    const user = await context.getUserCaller(bot);

    /*
    NOTE: Not currently implemented.

    // special treatment if new chat member:
    if ('new_chat_members' in msg) {
        ...
    }
    */

    if (!user.hasRights(rights)) return;

    if (!(redirect === undefined)) {
        return action_on_redirect(bot, context, arguments, redirect, text, options);
    }

    switch (command) {
        case command.match(/^\/pin(?:|_(.*))$/)?.input:
            const [ flag ] = arguments;
            if (flag === 'all') {
                return action_on_pin_all_languages(bot, context, text, options);
            }
            return action_on_pin_one_language(bot, context, arguments, text, options);
        case '/hello':
            const { debug } = options;
            if (debug) {
                return action_on_hello(bot, context, user, arguments, text, options);
            }
        case '/help':
            return action_on_help(bot, context, arguments, text, options);
        default:
            return action_delete_and_ignore();
    }
};

/****************************************************************
 * EXPORTS
 ****************************************************************/

module.exports = {
    universal_action,
};
