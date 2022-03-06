/****************************************************************
 * IMPORTS
 ****************************************************************/

//

/****************************************************************
 * METHODS
 ****************************************************************/

class User {
    first_name;
    kind;

    constructor(data) {
        const { user, status } = data;
        const {id, is_bot, first_name, username, language_code} = user;
        this.id = id;
        this.is_bot = is_bot;
        this.first_name = first_name;
        this.username = username;
        this.lang = language_code;
        this.kind = status;
    }

    isBot() { return this.is_bot }

    getId() { return this.id }

    getLanguage() { return this.lang }


    getUserName() { return this.username }

    getUserNameWithReference() { return '@' + this.username }

    getFirstName() { return this.first_name };

    getKind() { return this.kind; }

    hasRights(rights) { return rights.includes(this.kind); }

    toRepr() {
        return {
            id:         this.id,
            is_bot:     this.is_bot,
            first_name: this.first_name,
            username:   this.getUserNameWithReference(),
            lang:       this.lang,
            kind:       this.kind,
        };
    }

    toString() { return JSON.stringify(this.toRepr()); }
}

/****************************************************************
 * EXPORTS
 ****************************************************************/

module.exports = {
    User,
};
