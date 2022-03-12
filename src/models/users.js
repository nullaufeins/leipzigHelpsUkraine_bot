/****************************************************************
 * IMPORTS
 ****************************************************************/

 const { CENSOR_ATTRIBUTE } = require('./../core/logging.js');

/****************************************************************
 * METHODS
 ****************************************************************/

class User {
    first_name;
    kind;

    constructor(data) {
        const { user, status } = data;
        const {id, is_bot, first_name, username, language_code} = user || {};
        this.id = id;
        this.is_bot = is_bot;
        this.first_name = first_name;
        this.username = username;
        this.lang = language_code;
        this.user_type = status;
    }

    isBot() { return this.is_bot }

    getId() { return this.id }

    getLanguage() { return this.lang }


    getUserName() { return this.username }

    getUserNameWithReference() { return '@' + this.username }

    getFirstName() { return this.first_name };

    getUserType() { return this.user_type; }

    hasRights(rights) { return rights.includes(this.user_type); }

    toRepr() {
        return {
            id:         this.id,
            user_type:  this.user_type,
            is_bot:     this.is_bot,
            first_name: this.first_name,
            username:   this.getUserNameWithReference(),
            lang:       this.lang,
        };
    }

    toString() { return JSON.stringify(this.toRepr()); }

    /********
     * Provides a censored representation of User.
     * - censors `first_name`.
     * - censors `username` <==> `full_censor=true` passed as argument.
     *
     * NOTE: `first_name` forcibly censored as we never want to log this.
     * The `username` is not necessarily sensitive information.
     ********/
    toCensoredRepr(full_censor=false) {
        return {
            id:         this.id,
            user_type:  this.user_type,
            is_bot:     this.is_bot,
            first_name: CENSOR_ATTRIBUTE,
            // only censor censor if absolutely necessary:
            username:   full_censor === false ? this.getUserName() : CENSOR_ATTRIBUTE,
            lang:       this.lang,
        }
    }

    /********
     * Provides a censored representation of User.
     * - censors `first_name`.
     * - censors `username` <==> `full_censor=true` passed as argument.
     *
     * NOTE: `first_name` forcibly censored as we never want to log this.
     * The `username` is not necessarily sensitive information.
     ********/
    toCensoredString(full_censor=false) { return JSON.stringify(this.toCensoredRepr(full_censor)); }
}

/****************************************************************
 * EXPORTS
 ****************************************************************/

module.exports = {
    User,
};
