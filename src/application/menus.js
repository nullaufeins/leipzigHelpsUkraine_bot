/****************************************************************
 * IMPORTS
 ****************************************************************/

const {
    COMMANDS,
    get_translation
} = require.main.require('./setup/config.js');

/****************************************************************
 * METHODS
 ****************************************************************/

// Creates inline keyboard categories for the user to select from
const get_main_menu = (lang) => {
    let rows = [];
    let count = 0;
    let row_index = 0;
    for (const {keyword, hidden, new_row} of COMMANDS) {
        if (hidden) continue;
        if (count > 0 && new_row) {
            row_index += 1;
        }
        if (rows.length <= row_index) {
            rows.push([]);
        }
        const callback_data = keyword;
        const text = get_translation(lang, keyword);
        rows[row_index].push({text, callback_data});
        count += 1;
    }
    return {
        reply_markup: {
            // remove_keyboard: true,
            inline_keyboard: rows,
        },
    };
};

/****************************************************************
 * EXPORTS
 ****************************************************************/

module.exports = {
    get_main_menu,
};
