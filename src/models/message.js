/****************************************************************
 * IMPORTS
 ****************************************************************/

 const {
    CENSOR_ATTRIBUTE,
    censorMessage,
} = require('./../core/logging.js');
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
        this.timestamp = typeof date === 'number' ? date * 1000 : undefined;
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

    /********
     * Returns timestamp in ms
     ********/
    getTimestamp() { return this.timestamp; }

    /********
     * Returns User class, if data can be retrieved or else undefined.
     ********/
    async getUser(bot) {
        return bot.telegram.getChatMember(this.chatId, this.userId)
            .then((data) => new User(data))
            .catch((_) => {return undefined});
    }

    messageTooOld(t, expiry) {
        return (typeof this.timestamp === 'number') ? (this.timestamp + expiry < t) : true;
    }

    toRepr() {
        return {
            timestamp: this.timestamp,
            text:      this.text,
            lang:      this.lang,
            is_bot:    this.is_bot,
            messageId: this.messageId,
            chatId:    this.chatId,
            userId:    this.userId,
        }
    }

    toString() { return JSON.stringify(this.toRepr()); }

    /********
     * Provides a censored representation of Message:
     * - text` content of message partially censored.
     * - fully censored, if `full_censor=true` passed as argument.
     ********/
    toCensoredRepr(full_censor=false) {
        return {
            timestamp: this.timestamp,
            text:      full_censor === false ? censorMessage(this.text) : CENSOR_ATTRIBUTE,
            lang:      this.lang,
            is_bot:    this.is_bot,
            messageId: this.messageId,
            chatId:    this.chatId,
            userId:    this.userId,
        }
    }

    /********
     * Provides a censored representation of Message:
     * - text` content of message partially censored.
     * - fully censored, if `full_censor=true` passed as argument.
     ********/
    toCensoredString(full_censor) { return JSON.stringify(this.toCensoredRepr(full_censor)); }
}

/****************************************************************
 * EXPORTS
 ****************************************************************/

module.exports = {
    Message
};
