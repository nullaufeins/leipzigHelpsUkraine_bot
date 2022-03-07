/****************************************************************
 * IMPORTS
 ****************************************************************/

const { CombineErrors } = require('./../core/logging.js');
const {
    remove_message,
    send_message,
    send_message_as_overwrite,
} = require('../models/operations.js');

/****************************************************************
 * METHODS generic actions
 ****************************************************************/

/********
 * This allows for a complex chain of promises, which attempts to remove a message first
 * then if an error occurs, this is temporarily ignored, the desired action is taken,
 * and then the error is thrown again (combined with any subsequent errors from the action).
 ********/
const remove_temporarily_ignore_errors_then_do_action = async(bot, context, action) => {
    context.track('basic-action:delete');
    return remove_message(bot, context.getCallerMessage())
        // NOTE: if caught, will guaranteed not proceed to 'then' block:
        .catch((err) => {
            return action()
                .catch((err2) => {throw CombineErrors(err, err2)})
                .then(() => {throw err});
        })
        .then(action);
}

/****************************************************************
 * METHODS basic actions
 ****************************************************************/

const action_empty = async () => {
    // return resolved with value false to indicated that no action was taken.
    return Promise.resolve([false, undefined]);
};

const action_ignore = async (context) => {
    context.track('basic-action:ignore');
    // return resolved with value false to indicated that no action was taken.
    return action_empty();
};

const action_ignore_with_error = async (text) => {
    context.track('basic-action:ignore-with-error');
    return Promise.reject(text || 'Something went wrong. Ignoring.');
};

const action_delete_and_ignore = async (bot, context) => {
    return remove_temporarily_ignore_errors_then_do_action(bot, context, () => {
        context.track('basic-action:ignore');
        return Promise.resolve([false, undefined]);
    });
};

const action_delete_and_ignore_with_error = async (bot, context, text) => {
    return remove_temporarily_ignore_errors_then_do_action(bot, context, () => {
        context.track('basic-action:ignore-with-error');
        return Promise.reject(text || 'Something went wrong. Ignoring.');
    });
};

const action_send_message = async (bot, context, text, options, { delete_calls }) => {
    if (delete_calls) {
        return remove_temporarily_ignore_errors_then_do_action(bot, context, () => {
            context.track('basic-action:new-post');
            return send_message(bot, context.getCallerMessage(), text, options);
        });
    } else {
        context.track('basic-action:edit-post');
        return send_message_as_overwrite(bot, context.getCallerMessage(), text, options);
    }
};

/****************************************************************
 * EXPORTS
 ****************************************************************/

module.exports = {
    remove_temporarily_ignore_errors_then_do_action,
    action_empty,
    action_ignore,
    action_ignore_with_error,
    action_delete_and_ignore,
    action_delete_and_ignore_with_error,
    action_send_message,
};
