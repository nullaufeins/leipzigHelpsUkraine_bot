/****************************************************************
 * IMPORTS
 ****************************************************************/

const { Message } = require('./message.js');
const { Trace } = require('./trace.js');
const { User } = require('./users.js');

/****************************************************************
 * Class Çall Context
 ****************************************************************/

class CallContext {
    constructor(ctx) {
        this.trace = new Trace();
        this.botname = ctx.botInfo.username;
        const msg = ctx.update.message;
        this.caller_msg = new Message(msg);
        const { reply_to_message } = msg;
        this.reply_to_msg = reply_to_message === undefined ? undefined : new Message(reply_to_message);
        this.userCaller = undefined;
        this.userReplyTo = undefined;
        this.groupId = undefined;
        this.groupTitle = undefined;
    }

    track(x) { this.trace.add(x); }

    async getGroupInfos(bot) {
        const chatId = this.caller_msg.getChatId();
        const chat = await bot.telegram.getChat(chatId)
            .catch((_) => {return undefined});
        this.groupId = (chat || {}).id; // === chatId
        this.groupTitle = (chat || {}).title;
    }

    getCallerMessage() { return this.caller_msg; }

    getReplyToMessage() { return this.reply_to_msg; }

    getBotname() { return this.botname; }

    toRepr() {
        return {
            botname: this.botname,
            group_id: this.groupId,
            group_title: this.groupTitle,
            message: this.caller_msg.toRepr(),
            reply_to: this.reply_to_msg instanceof Message ? this.reply_to_msg.toRepr() : undefined,
            trace: this.trace.toRepr(),
        }
    }

    toString() { return JSON.stringify(this.toRepr()); }

    /********
     * Provides a censored representation of CallContext.
     * - censors `message` attributes (fully if `full_censor=true`).
     * - fully censors `reply_to` message attributes.^
     *
     * NOTE: ^forced, as we never want to log text contents of this message.
     ********/
    toCensoredRepr(full_censor=false) {
        return {
            botname: this.botname,
            group_id: this.groupId,
            group_title: this.groupTitle,
            message: this.caller_msg.toCensoredRepr(full_censor),
            reply_to: this.reply_to_msg instanceof Message ? this.reply_to_msg.toCensoredRepr(true) : undefined,
            trace: this.trace.toRepr(),
        }
    }

    /********
     * Provides a censored representation of CallContext.
     * - censors `message` attributes (fully if `full_censor=true`).
     * - fully censors `reply_to` message attributes.^
     *
     * NOTE: ^forced, as we never want to log text contents of this message.
     ********/
    toCensoredString(full_censor=false) { return JSON.stringify(this.toCensoredRepr(full_censor)); }

    /********
     * Methods related just to caller
     ********/

    getTextCaller() { return this.caller_msg.getText(); }

    getLanguageCaller() { return this.caller_msg.getLanguage(); }

    isBotCaller() { return this.caller_msg.isBot(); }

    /********
     * Returns true/false <==> user is/is not anon admin.
     * If information cannot be obtained, returns undefined.
     ********/
    async isGroupAdminCaller(bot) {
        const user = await this.getUserCaller(bot);
        if (user instanceof User) {
            return user.isBot() === true && user.getFirstName() === 'Group' && user.getUserName() === 'GroupAnonymousBot';
        }
        return undefined;
    }

    /********
     * Returns User class for caller, if data can be retrieved or else undefined.
     ********/
    async getUserCaller(bot) {
        if (this.userCaller === undefined) {
            const user = await this.caller_msg.getUser(bot);
            this.userCaller = user;
        }
        return this.userCaller;
    }

    messageTooOldCaller(t, expiry) { return this.caller_msg.messageTooOld(t, expiry); }

    /********
     * Methods related just to message_replied to
     ********/

    getTextMessageRepliedTo() { return this.reply_to_msg instanceof Message ? this.reply_to_msg.getText() : undefined; }

    getLanguageMessageRepliedTo() { return this.reply_to_msg instanceof Message ? this.reply_to_msg.getLanguage() : undefined; }

    isBotMessageRepliedTo() { return this.reply_to_msg instanceof Message ? this.reply_to_msg.isBot() : undefined; }

    /********
     * Returns User class for message replied to, if data can be retrieved or else undefined.
     ********/
    async getUserMessageRepliedTo(bot) {
        if (this.userReplyTo === undefined) {
            const user = this.reply_to_msg instanceof Message ? await this.reply_to_msg.getUser(bot) : undefined;
            this.userReplyTo = user;
        }
        return this.userReplyTo;
    }

    messageTooOldMessageRepliedTo(t, expiry) { return this.reply_to_msg instanceof Message ? this.reply_to_msg.messageTooOld(t, expiry) : undefined; }
}

/****************************************************************
 * EXPORTS
 ****************************************************************/

module.exports = {
    CallContext
};
