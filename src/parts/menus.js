/****************************************************************
 * IMPORTS
 ****************************************************************/

const {
    COMMANDS,
    get_translation
} = require.main.require('./src/setup/config.js');

/****************************************************************
 * METHODS
 ****************************************************************/

// Creates inline keyboard categories for the user to select from
const get_main_menu_inline = (lang, reply_to_msg = undefined) => {
    return {
        reply_markup: {
            inline_keyboard: create_rows(lang),
            disable_notification: true,
            parse_mode: 'MarkdownV2',
        },
        reply_to_message_id: reply_to_msg === undefined ? undefined : reply_to_msg.message_id,
    };
};

const get_main_menu_hidden = (lang, reply_to_msg = undefined) => (
    {
        reply_markup: {
            keyboard: create_rows(lang),
            resize_keyboard: true,
            one_time_keyboard: true,
            disable_notification: true,
            parse_mode: 'MarkdownV2',
        },
        reply_to_message_id: reply_to_msg === undefined ? undefined : reply_to_msg.message_id,
    }
);

const get_message_options_basic = (reply_to_msg = undefined) => (
    {
        reply_markup: {
            disable_notification: true,
            parse_mode: 'MarkdownV2',
        },
        reply_to_message_id: reply_to_msg === undefined ? undefined : reply_to_msg.message_id,
    }
);

/****************************************************************
 * AUXILIARY METHODS
 ****************************************************************/

const create_rows = (lang) => {
    let rows = [];
    let count = 0;
    let row_index = 0;
    for (const { aspects, menu } of COMMANDS) {
        const { redirect } = aspects;
        if (!redirect || !menu) continue;
        const { keyword, new_row } = menu;
        if (count > 0 && new_row) row_index += 1;
        if (rows.length <= row_index) rows.push([]);
        const text = get_translation(lang, keyword);
        rows[row_index].push({text, url: create_url(redirect)});
        count += 1;
    }
    return rows;
};

const create_url = (text) => {
    let pattern = /^\@(.*)$/;
    if (pattern.test(text)) {
        return text.replace(pattern, `https://t.me/$1`);
    }
    pattern = /^[^:]+:\/{2}.*/;
    if (pattern.test(text)) {
        return text;
    }
    return text;
};

/****************************************************************
 * EXPORTS
 ****************************************************************/

module.exports = {
    get_main_menu_inline,
    get_main_menu_hidden,
    get_message_options_basic,
};
