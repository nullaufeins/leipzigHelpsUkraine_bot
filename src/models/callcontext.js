/****************************************************************
 * IMPORTS
 ****************************************************************/

const { Message } = require('./message.js');
const { Trace } = require('./trace.js');

/****************************************************************
 * Class Çall Context
 ****************************************************************/

class CallContext {
    constructor(ctx) {
        this.trace = new Trace();
        this.botname = ctx.botInfo.username;
        const msg = ctx.update.message;
        this.caller_msg = new Message(msg);
        this.reply_to_msg = new Message(msg.reply_to_message);
    }

    track(x) { this.trace.add(x); }

    getCallerMessage() { return this.caller_msg; }

    getReplyToMessage() { return this.reply_to_msg; }

    getBotname() { return this.botname; }

    toRepr() {
        return {
            botname: this.botname,
            message: this.caller_msg.toRepr(),
            reply_to_message: this.reply_to_msg.toRepr(),
            tracking: this.trace.toRepr(),
        }
    }

    toString() { return JSON.stringify(this.toRepr()); }

    /********
     * Methods related just to caller
     ********/

    getTextCaller() { return this.caller_msg.getText(); }

    getLanguageCaller() { return this.caller_msg.getLanguage(); }

    isBotCaller() { return this.caller_msg.isBot(); }

    async getUserCaller(bot) { return this.caller_msg.getUser(bot); }

    messageTooOldCaller(t, expiry) { return this.caller_msg.messageTooOld(t, expiry); }

    /********
     * Methods related just to message_replied to
     ********/

    getTextMessageRepliedTo() { return this.reply_to_msg.getText(); }

    getLanguageMessageRepliedTo() { return this.reply_to_msg.getLanguage(); }

    isBotMessageRepliedTo() { return this.reply_to_msg.isBot(); }

    async getUserMessageRepliedTo(bot) { return this.reply_to_msg.getUser(bot); }

    messageTooOldMessageRepliedTo(t, expiry) { return this.reply_to_msg.messageTooOld(t, expiry); }
}

/****************************************************************
 * EXPORTS
 ****************************************************************/

module.exports = {
    CallContext
};
