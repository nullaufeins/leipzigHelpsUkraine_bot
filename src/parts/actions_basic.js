/****************************************************************
 * IMPORTS
 ****************************************************************/

const {
    remove_message,
    send_message,
    send_message_as_overwrite,
} = require('../models/operations.js');

/****************************************************************
 * METHODS basic and generic actions
 ****************************************************************/

const action_ignore = async (context) => {
    context.track('basic-action:ignore');
    // return resolved with value false to indicated that no action was taken.
    return Promise.resolve([false, undefined]);
};

const action_ignore_with_error = async (text) => {
    context.track('basic-action:ignore-with-error');
    return Promise.reject(text || 'Something went wrong. Ignoring.');
};

const action_delete_and_ignore = async (bot, context) => {
    context.track('basic-action:delete-and-ignore');
    return remove_message(bot, context.getCallerMessage());
};

const action_send_message = async (bot, context, text, options, { delete_calls }) => {
    if (delete_calls) {
        /********
         * NOTE: if this fails, this error will be caught at a higher level.
         * Do not catch here, as we want to force the bot to continue with the post,
         * even the if the deletion fails.
         ********/
        context.track('basic-action:delete-caller-msg');
        await remove_message(bot, context.getCallerMessage());
        context.track('basic-action:new-post');
        return send_message(bot, context.getCallerMessage(), text, options);
    } else {
        context.track('basic-action:edit-post');
        return send_message_as_overwrite(bot, context.getCallerMessage(), text, options);
    }
};

/****************************************************************
 * EXPORTS
 ****************************************************************/

module.exports = {
    action_ignore,
    action_ignore_with_error,
    action_delete_and_ignore,
    action_send_message,
};
