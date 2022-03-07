/****************************************************************
 * IMPORTS
 ****************************************************************/

const {
    split_non_empty_parts,
    take_one,
} = require('./../core/utils.js');
const { COMMANDS } = require('./../setup/config.js');

/****************************************************************
 * METHODS - pattern recognition
 ****************************************************************/

/****************
 * PATTERN_PRE - used inline when user explicity talks to bot.
 * recognises patterns (space after BOTNAME necessary!):
 *
 *    @BOTNAME COMMAND
 *    @BOTNAME /COMMAND
 *    @BOTNAME COMMAND arg1 arg2 ...
 *    @BOTNAME /COMMAND arg1 arg2 ...
 ****************/
const PATTERN_PRE = /^\s*\@(\S+)\s+\/?(\S.*)$/;
/****************
 * PATTERN_PRE - used via side menus, when user chooses a suggestion.
 * recognises patterns (space before @BOTNAME not necessary):
 *
 *    /COMMAND @BOTNAME
 ****************/
const PATTERN_POST = /^\s*\/([^\@\s]+)\s*\@(\S+)\s*$/;

const is_valid_communication_pre = (text) => (PATTERN_PRE.test(text));
const is_valid_communication_post = (text) => (PATTERN_POST.test(text));

/****************************************************************
 * METHODS - argument extraction
 ****************************************************************/

const extra_arguments_pre = (text) => {
    const pattern = PATTERN_PRE;
    if (pattern.test(text)) {
        const botname = text.replace(pattern, `$1`).trim();
        const text1 = text.replace(pattern, `$2`).trim();
        const [command, arguments] = take_one(split_non_empty_parts(text1));
        return { command: command || '', botname: botname, arguments, matches: true };
    }
    return { matches: false };
}

const extra_arguments_post = (text) => {
    const pattern = PATTERN_POST;
    if (pattern.test(text)) {
        const botname = text.replace(pattern, `$2`).trim();
        const command = text.replace(pattern, `$1`).trim();
        return { command: command, botname: botname, arguments: [], matches: true };
    }
    return { matches: false }
}

/****************
 * Usage of following commands:
 * ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 *  inputs:
 *    text    = raw text input
 *    botname = name of bot to be matched
 *  returns:
 *    text     = cleaned up text (removed any botname mention)
 *    botname  = botname recognised or else undefined
 *    verified = true/false if botname recognised and matches/not, else undefined
 ****************/
const extract_communication_aspects = (extra_arguments, text_, botname_) => {
    let { command, arguments, botname, matches } = extra_arguments(text_);

    const verified = (botname === undefined ? undefined : matches && (botname == botname_));
    return { command, arguments, verified };
}

const extract_botname_pre = (text, botname) => (extract_communication_aspects(extra_arguments_pre, text, botname));
const extract_botname_post = (text, botname) => (extract_communication_aspects(extra_arguments_post, text, botname));

/****************************************************************
 * METHODS - command filtration
 ****************************************************************/

const filter_commands_by_condition = (condition) => COMMANDS.filter(condition);
const filter_commands_by_match = (text) => (filter_commands_by_condition(({ aspects }) => {
    const { match } = aspects;
    return match.test(text);
}));

/****************************************************************
 * EXPORTS
 ****************************************************************/

module.exports = {
    is_valid_communication_pre,
    is_valid_communication_post,
    extract_botname_pre,
    extract_botname_post,
    filter_commands_by_condition,
    filter_commands_by_match,
};
