/****************************************************************
 * IMPORTS
 ****************************************************************/

//

/****************************************************************
 * DEFINITIONS
 ****************************************************************/

class TranslatedText {
    keyword;
    values;
    default;

    constructor(keyword, values, default_lang) {
        this.keyword = keyword;
        this.values = values;
        this.default = default_lang;
    }

    value(lang) {
        if (!(lang in this.values)) {
            // console.warn(`Keyword \x1b[1m${this.keyword}\x1b[0m has no \x1b[92;1m${lang}\x1b[0m-translation; -> default to \x1b[92;1m${this.default}\x1b[0m.`);
            lang = this.default;
        }
        return this.values[lang] || '';
    }
}

class TranslatedTexts {
    values;

    constructor(data, default_lang) {
        this.values = {};
        Object.entries(data).some(([keyword, tr]) => {
            this.values[keyword] = new TranslatedText(keyword, tr, default_lang);
        });
    }

    value(lang, keyword) {
        if (!(keyword in this.values)) {
            // console.error(`The keyword \x1b[1m${keyword}\x1b[0m has no translations!`);
            return undefined;
        }
        return this.values[keyword].value(lang);
    }
}

/****************************************************************
 * EXPORTS
 ****************************************************************/

module.exports = {
    TranslatedTexts
};
