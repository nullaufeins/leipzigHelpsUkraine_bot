/****************************************************************
 * IMPORTS
 ****************************************************************/

const { User } = require('./users.js');

/****************************************************************
 * Class Message
 ****************************************************************/

class Message {
    text;
    lang;
    is_bot;
    chatId;
    userId;
    messageId;

    constructor(msg) {
        const date = (msg || {}).date;
        this.date_posted = typeof date === 'number' ? date * 1000 : undefined;
        this.text = ((msg || {}).text || '').trim();
        this.lang = ((msg || {}).from || {}).language_code;
        this.is_bot = (((msg || {}).from) || {}).is_bot;
        // IDs:
        this.messageId = (msg || {}).message_id;
        this.chatId = ((msg || {}).chat || {}).id;
        this.userId = ((msg || {}).from || {}).id;
    }

    getChatId() { return this.chatId; }

    getMessageId() { return this.messageId; }

    getUserId() { return this.userId; }

    getIds() { return { chatId: this.chatId, userId: this.userId, messageId: this.messageId }; }

    getText() { return this.text; }

    getLanguage() { return this.lang; }

    isBot() { return this.is_bot; }

    // returns timestamp in ms
    getTimestamp() { return this.date_posted; }

    async getUser(bot) {
        return bot.telegram.getChatMember(this.chatId, this.userId)
            .then((data) => new User(data))
            .catch((_) => {return undefined});
    }

    messageTooOld(t, expiry) {
        return (typeof this.date_posted === 'number') ? (this.date_posted + expiry < t) : true;
    }

    toRepr() {
        return {
            data:      this.date_posted,
            text:      this.text,
            lang:      this.lang,
            is_bot:    this.is_bot,
            messageId: this.messageId,
            chatId:    this.chatId,
            userId:    this.userId,
        }
    }

    toString() { return JSON.stringify(this.toRepr()); }
}

/****************************************************************
 * EXPORTS
 ****************************************************************/

module.exports = {
    Message
};
