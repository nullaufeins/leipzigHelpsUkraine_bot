/****************************************************************
 * IMPORTS
 ****************************************************************/

const {
    is_valid_communication_pre,
    is_valid_communication_post,
    filter_commands_by_command_pre,
    filter_commands_by_command_post,
} = require('./../setup/comms.js');
const { logListenerErrorSilently } = require('./../core/logging.js');
const { CallContext } = require('./../models/callcontext.js');
const { universal_action } = require('./actions.js');
const {
    action_ignore,
    action_ignore_with_error,
} = require('./actions_basic.js');

/****************************************************************
 * META METHOD - decorate listener
 ****************************************************************/

const decorate_listener = (listener, bot, options) => {
    const { debug } = options;
    return async (ctx) => {
        const t = Date.now();
        const context = new CallContext(ctx);
        return listener(bot, context, t, options)
            // !!! logging only in debug mode during local testing !!!
            .then(([action_taken, _]) => {
                if (debug && (action_taken === true)) {
                    console.log('Current state', context.toRepr());
                }
            })
            // error logging (for live usage):
            .catch((err) => logListenerErrorSilently(context, err))
    }
}

/****************************************************************
 * METHODS - LISTENERS
 ****************************************************************/

const listener_on_callback_query = async (bot, context, t, options) => {
    return action_ignore_with_error(context, 'Listener not yet implemented');
};

/****************
 * Listens to all messages and decides if Bot has been spoken to
 * and if a command is to be carried out.
 *
 * See README-TECHNICAL.md.
 ****************/
const listener_on_text = async (bot, context, t, options) => {
    if (!(context.isBotCaller() === false)) return action_ignore(context);
    const { message_expiry } = options;

    if (context.messageTooOldCaller(t, message_expiry)) return action_ignore(context);
    const text = context.getTextCaller();

    if (is_valid_communication_pre(text)) {
        context.track('text-listener');
        const {commands, arguments} = filter_commands_by_command_pre(text, context.getBotname());
        if (commands.length > 0) return universal_action(bot, context, commands[0], arguments, options);
        // if invalid command:
        return action_ignore(context);
    } else if (text.startsWith(`/`)) {
        return listener_on_message(bot, context, t, options);
    } else {
        // if not potentially a command:
        return action_ignore(context);
    }
}

/****************
 * Handles inline user query.
 *
 * See README-TECHNICAL.md.
 ****************/
const listener_on_message = async (bot, context, t, options) => {
    if (!(context.isBotCaller() === false)) return action_ignore(context);

    const { message_expiry } = options;
    if (context.messageTooOldCaller(t, message_expiry)) return action_ignore(context);

    const text = context.getTextCaller();
    if (is_valid_communication_post(text)) {
        context.track('msg-listener');
        const {commands, arguments} = filter_commands_by_command_post(text, context.getBotname());
        if (commands.length > 0) return universal_action(bot, context, commands[0], arguments, options);
        // if invalid command:
        return action_ignore(context);
    } else {
        // if not potentially a command:
        return action_ignore(context);
    }
}

/****************************************************************
 * EXPORTS
 ****************************************************************/

module.exports = {
    decorate_listener,
    listener_on_callback_query,
    listener_on_text,
    listener_on_message,
};
