/****************************************************************
 * IMPORTS
 ****************************************************************/

const { try_action1_silently_then_perform_action2 } = require('./../core/utils.js');

const {
    remove_message,
    send_message,
    send_message_as_overwrite,
} = require('./../models/operations.js');

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
    return try_action1_silently_then_perform_action2(
    async () => {
        context.track('basic-action:delete');
        return remove_message(bot, context.getCallerMessage())
    },
    async () => {
        context.track('basic-action:ignore');
        return Promise.resolve([false, undefined]);
    });
};

const action_delete_and_ignore_with_error = async (bot, context, text) => {
    return try_action1_silently_then_perform_action2(
    async () => {
        context.track('basic-action:delete');
        return remove_message(bot, context.getCallerMessage())
    },
    async () => {
        context.track('basic-action:ignore-with-error');
        return Promise.reject(text || 'Something went wrong. Ignoring.');
    });
};

const action_send_message = async (bot, context, text, options, { delete_calls }) => {
    if (delete_calls) {
        return try_action1_silently_then_perform_action2(
        async () => {
            context.track('basic-action:delete');
            return remove_message(bot, context.getCallerMessage())
        },
        async () => {
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
    action_empty,
    action_ignore,
    action_ignore_with_error,
    action_delete_and_ignore,
    action_delete_and_ignore_with_error,
    action_send_message,
};
