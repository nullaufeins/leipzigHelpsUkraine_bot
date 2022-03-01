/****************************************************************
 * IMPORTS
 ****************************************************************/

//

/****************************************************************
 * METHODS
 ****************************************************************/

const user_in_context_is_bot = (ctx) => (ctx.update.message.from.is_bot);

const get_user_from_context = (bot, ctx) => {
    const chatId = ctx.update.message.chat.id;
    const userId = ctx.update.message.from.id;
    return bot.telegram.getChatMember(chatId, userId);
};

const user_has_rights = (user, rights) => {
    const type = user.status;
    return rights.includes(type);
};

/****************************************************************
 * EXPORTS
 ****************************************************************/

module.exports = {
    get_user_from_context,
    user_in_context_is_bot,
    user_has_rights,
};
