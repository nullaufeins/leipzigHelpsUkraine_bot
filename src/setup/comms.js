/****************************************************************
 * IMPORTS
 ****************************************************************/

const {
    split_non_empty_parts,
    take_one,
} = require.main.require('./src/core/utils.js');
const { COMMANDS } = require.main.require('./src/setup/config.js');

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

// filters commands by matching criteria and returns arguments:
const filter_commands_by_command = (extraction, text_, botname) => {
    // extract information about bot addressed:
    const { command, arguments, verified } = extraction(text_, botname);

    // reject, if a botname is recognised but does not match:
    if (verified === false) return { commands: [], arguments };

    /****
     * Conditions for a command to be included in filter:
     *
     * 1. if strict mode, botnames must match (i.e. verified == true must hold); and
     * 2. command pattern must be matched.
     ****/
    const condition = ({ aspects }) => {
        const { match, strict } = aspects;
        return ((!strict || verified === true) && match.test(command));
    };
    return { commands: filter_commands_by_condition(condition), arguments };
}

const filter_commands_by_command_pre = (text, botname) => (filter_commands_by_command(extract_botname_pre, text, botname));
const filter_commands_by_command_post = (text, botname) => (filter_commands_by_command(extract_botname_post, text, botname));

/****************************************************************
 * EXPORTS
 ****************************************************************/

module.exports = {
    is_valid_communication_pre,
    is_valid_communication_post,
    filter_commands_by_command_pre,
    filter_commands_by_command_post,
};
