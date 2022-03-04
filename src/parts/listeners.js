/****************************************************************
 * IMPORTS
 ****************************************************************/

const {
    is_valid_communication_pre,
    is_valid_communication_post,
    filter_commands_by_command_pre,
    filter_commands_by_command_post,
} = require.main.require('./src/setup/comms.js');
const { message_too_old } = require.main.require('./src/parts/operations.js');
const {
    user_in_context_is_bot,
} = require.main.require('./src/parts/users.js');
const {
    universal_action,
    action_ignore,
    action_delete_and_ignore,
} = require.main.require('./src/parts/actions.js');

/****************************************************************
 * METHODS - LISTENERS
 ****************************************************************/

const listener_on_callback_query = async () => {
    console.warn('Not yet implemented');
};

const listener_on_text = async (bot, ctx, t, options) => {
    // do nothing if bot:
    if (user_in_context_is_bot(ctx)) return action_ignore();
    // otherwise ...
    const msg = ctx.update.message;
    const text = (msg.text || '').trim();
    if (is_valid_communication_pre(text)) {
        // if too old, delete and return:
        const { message_expiry } = options;
        if (message_too_old(msg, t, message_expiry)) {
            return action_delete_and_ignore(bot, msg);
        }
        const botname = ctx.botInfo.username;
        const {commands, arguments} = filter_commands_by_command_pre(text, botname);
        if (commands.length > 0) {
            return universal_action(bot, ctx, commands[0], arguments, options);
        }
        // if invalid command, delete and return:
        return action_delete_and_ignore(bot, msg);
    } else if (text.startsWith(`/`)) {
        return listener_on_message(bot, ctx, t, options);
    }
    // do nothing if not potentially a command:
    return action_ignore(bot, msg);
}

// handles inline user query:
const listener_on_message = async (bot, ctx, t, options) => {
    // do nothing if bot:
    if (user_in_context_is_bot(ctx)) return action_ignore();
    // otherwise ...
    const msg = ctx.update.message;
    const text = (msg.text || '').trim();
    if (is_valid_communication_post(text)) {
        // if too old, delete and return
        const { message_expiry }  = options;
        if (message_too_old(msg, t, message_expiry)) {
            return action_delete_and_ignore(bot, msg);
        }
        const botname = ctx.botInfo.username;
        const {commands, arguments} = filter_commands_by_command_post(text, botname);
        if (commands.length > 0) {
            return universal_action(bot, ctx, commands[0], arguments, options);
        }
        // if invalid command, delete and return:
        return action_delete_and_ignore(bot, msg);
    }
    // do nothing if not potentially a command:
    return action_ignore(bot, msg);
}

/****************************************************************
 * EXPORTS
 ****************************************************************/

module.exports = {
    listener_on_callback_query,
    listener_on_text,
    listener_on_message,
};
