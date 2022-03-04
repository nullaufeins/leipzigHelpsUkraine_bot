/****************************************************************
 * IMPORTS
 ****************************************************************/

const {
    is_valid_communication_pre,
    filter_commands_by_command_pre,
    filter_commands_by_command_post,
} = require.main.require('./src/setup/comms.js');
const { message_too_old } = require.main.require('./src/parts/operations.js');
const {
    user_in_context_is_bot,
} = require.main.require('./src/parts/users.js');
const {
    universal_action,
} = require.main.require('./src/parts/actions.js');

/****************************************************************
 * METHODS - LISTENERS
 ****************************************************************/

const listener_on_callback_query = async () => {
    console.warn('Not yet implemented');
};

const listener_on_text = async (bot, ctx, t, { debug, message_expiry }) => {
    if (user_in_context_is_bot(ctx)) return;
    const msg = ctx.update.message;
    if (message_too_old(msg, t, message_expiry)) return;
    const text = (msg.text || '').trim();
    if (is_valid_communication_pre(text)) {
        const botname = ctx.botInfo.username;
        const {commands, arguments} = filter_commands_by_command_pre(text, botname);
        if (commands.length == 0) return;
        return universal_action(bot, ctx, commands[0], arguments, { debug });
    } else if (text.startsWith(`/`)) {
        return listener_on_message(bot, ctx, { debug });
    }
    // else reject, as not valid communication to bot.
}

// handles inline user query:
const listener_on_message = async (bot, ctx, t, { debug, message_expiry }) => {
    if (user_in_context_is_bot(ctx)) return;
    const msg = ctx.update.message;
    if (message_too_old(msg, t, message_expiry)) return;
    const text = (msg.text || '').trim();
    const botname = ctx.botInfo.username;
    const {commands, arguments} = filter_commands_by_command_post(text, botname);
    if (commands.length == 0) return;
    return universal_action(bot, ctx, commands[0], arguments, { debug });
}

/****************************************************************
 * EXPORTS
 ****************************************************************/

module.exports = {
    listener_on_callback_query,
    listener_on_text,
    listener_on_message,
};
