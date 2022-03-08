/****************************************************************
 * IMPORTS
 ****************************************************************/

const { Message } = require('./message.js');
const { Trace } = require('./trace.js');
const { CENSOR_ATTRIBUTE } = require('./../core/logging.js');

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
        this.userCaller = undefined;
        this.userReplyTo = undefined;
        this.groupId = '';
        this.groupTitle = '';
    }

    track(x) { this.trace.add(x); }

    async getGroupInfos(bot) {
        const chatId = this.caller_msg.getChatId();
        const chat = await bot.telegram.getChat(chatId)
            .catch((_) => {return undefined});
        this.groupId = (chat || {}).id; // === chatId
        this.groupTitle = (chat || {}).title;
        return !(chat === undefined);
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
            reply_to: this.reply_to_msg.toRepr(),
            trace: this.trace.toRepr(),
        }
    }

    toString() { return JSON.stringify(this.toRepr()); }

    toCensoredRepr(full_censor=false) {
        return {
            botname: this.botname,
            group_id: CENSOR_ATTRIBUTE,
            group_title: full_censor === false ? this.groupTitle : CENSOR_ATTRIBUTE,
            message: this.caller_msg.toCensoredRepr(full_censor),
            // NOTE: fully censor the messaged replied to, regardless:
            reply_to: this.reply_to_msg.toCensoredRepr(true),
            trace: this.trace.toRepr(),
        }
    }

    toCensoredString(full_censor=false) { return JSON.stringify(this.toCensoredRepr(full_censor)); }

    /********
     * Methods related just to caller
     ********/

    getTextCaller() { return this.caller_msg.getText(); }

    getLanguageCaller() { return this.caller_msg.getLanguage(); }

    isBotCaller() { return this.caller_msg.isBot(); }

    async isGroupAdminCaller() {
        const user = await this.getUserCaller();
        return user.getFirstName() === 'Group'
            && user.getUserName() === 'GroupAnonymousBot';
    }

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
