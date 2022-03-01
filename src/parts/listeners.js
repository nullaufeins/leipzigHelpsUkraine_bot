/****************************************************************
 * IMPORTS
 ****************************************************************/

const {
    get_command_by_keyword,
    get_command_by_command,
} = require.main.require('./src/setup/config.js');
const {
    get_user_from_context,
    user_in_context_is_bot,
} = require.main.require('./src/parts/users.js');
const {
    universal_action,
} = require.main.require('./src/parts/actions.js');

/****************************************************************
 * METHODS - LISTENERS
 ****************************************************************/

// NOTE: chatId = uid for target chat / username of the target channel (in format @channelusername)
// handles user button push:
const listener_on_callback_query = async (bot, ctx, { debug }) => {
    if (user_in_context_is_bot(ctx)) return;
    const msg = ctx.update.message;
    const keyword = (msg.data || '').trim();
    const commands = get_command_by_keyword(keyword);
    if (commands.length == 0) return;
    return universal_action(bot, ctx, commands[0], { debug });
};

// handles inline user query:
const listener_on_message = async (bot, ctx, { debug }) => {
    if (user_in_context_is_bot(ctx)) return;
    const msg = ctx.update.message;
    const cmd = (msg.text || '').trim();
    const commands = get_command_by_command(cmd);
    if (commands.length == 0) return;
    return universal_action(bot, ctx, commands[0], { debug });
}

/****************************************************************
 * EXPORTS
 ****************************************************************/

module.exports = {
    listener_on_callback_query,
    listener_on_message,
};
