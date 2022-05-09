#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from thirdparty.code import *;
from thirdparty.types import *;

from src.core.calls import *;
from src.core.utils import *;
from src.setup.config import *;
from src.api import *;
from src.models.config import *;
from src.models.telegram import *;
from src.behaviour.recognition import *;
from src.behaviour.layout.menus import *;
from src.behaviour.actions.basic import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'action_on_pin_one_language',
    'action_on_pin_all_languages',
    'action_on_hello',
    'action_on_help',
    'action_on_redirect',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ACTION pin help menu - one language
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@run_safely()
def action_on_pin_one_language(
    bot:          MyBot,
    context:      CallContext,
    command_text: CommandText,
    lang_flag:    Optional[str],
) -> Result[CallValue, CallError]:
    context.track('action:pin');

    # post menu:
    lang = getLanguageByPriorityBasic(
        lang_config = command_text.lang,
        lang_flag   = lang_flag,
    );
    text = get_translation(keyword=command_text.keyword, lang=lang);
    layout = get_menu_inline(lang=lang);

    # pin menu:
    msg = context.getCallerMessage();
    return keep_calm_and_carry_on(
        context.track_function('basic-action:delete') (
            lambda: posts.remove_message(bot=bot, msg=msg)
        ),
        lambda: posts.send_and_pin_message(bot=bot, msg=msg, text=text, layout=layout)
    );

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ACTION pin help menu - all languages
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@run_safely()
def action_on_pin_all_languages(
    bot:          MyBot,
    context:      CallContext,
    command_text: CommandText,
) -> Result[CallValue, CallError]:
    context.track('action:pin-all');
    msg = context.getCallerMessage();
    return keep_calm_and_carry_on(
        context.track_function('basic-action:delete')(
            lambda: posts.remove_message(bot=bot, msg=msg)
        ),
        ################
        # NOTE: This has to be done via wrappers (current implementation) otherwise
        # every action will be triggered with only final values of loop-values.
        ################
        *[
            each_action_for_pin_all(
                bot     = bot,
                msg     = msg,
                keyword = command_text.keyword,
                index   = index,
                lang    = lang,
            )
            for index, lang in enumerate(SUPPORTED_LANGUAGES)
        ],
    );

# the following wraps the individually created actions:
def each_action_for_pin_all(
    bot:     MyBot,
    msg:     Message,
    keyword: str,
    index:   int,
    lang:    str,
):
    text = get_translation(keyword=keyword, lang=lang);
    layout = get_menu_inline(lang=lang);
    if index == 0:
        # post then pin 1st menu:
        return lambda: posts.send_and_pin_message(bot=bot, msg=msg, text=text, layout=layout);
    else:
        # post 2nd, 3rd, etc. menus without pinning:
        return lambda: posts.send_message(bot=bot, msg=msg, text=text, layout=layout);

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ACTION greet user
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@run_safely()
def action_on_hello(
    bot:             MyBot,
    context:         CallContext,
    user:            Option[User],
    user_replied_to: Option[User],
    command_text:    CommandText,
    lang_flag:       Optional[str],
    app_options:     AppOptions,
) -> Result[CallValue, CallError]:
    context.track('action:hello');

    # decide whether to reply to caller or replied-to-user (if exists):
    name = Nothing();
    if isinstance(user_replied_to, Some):
        name = user_replied_to.unwrap().getFirstName();
    elif isinstance(user, Some):
        name = user.unwrap().getFirstName();
    else:
        return action_ignore_with_error(context=context, text='No user information available!');

    # construct greeting:
    lang = getLanguageByPriorityInContext(
        context     = context,
        lang_config = command_text.lang,
        lang_flag   = lang_flag,
    );
    greet = get_translation(keyword=command_text.keyword, lang=lang, missing=r'Hi, %!');
    text = greet % name;
    layout = get_message_options_basic(context.getReplyToMessage());

    # post text:
    return action_send_message(bot=bot, context=context, text=text, layout=layout, app_options=app_options);

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ACTION help
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@run_safely()
def action_on_help(
    bot:          MyBot,
    context:      CallContext,
    command_text: CommandText,
    lang_flag:    Optional[str],
    app_options:  AppOptions,
) -> Result[CallValue, CallError]:
    context.track('action:help');

    # post menu:
    lang = getLanguageByPriorityInContextIgnoreCaller(
        context     = context,
        lang_config = command_text.lang,
        lang_flag   = lang_flag
    );
    reply_to_msg = context.getReplyToMessage();
    text = get_translation(keyword=command_text.keyword, lang=lang);
    layout = get_menu_inline(lang=lang, reply_to_msg=reply_to_msg);

    return action_send_message(bot=bot, context=context, text=text, layout=layout, app_options=app_options);

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ACTION redirect
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@run_safely()
def action_on_redirect(
    bot:          MyBot,
    context:      CallContext,
    command_text: CommandText,
    lang_flag:    Optional[str],
    redirect:     CommandRedirect,
    app_options:  AppOptions,
) -> Result[CallValue, CallError]:
    context.track('action:redirect');

    # post text with link:
    lang = getLanguageByPriorityInContextIgnoreCaller(
        context     = context,
        lang_config = command_text.lang,
        lang_flag   = lang_flag
    );
    message = get_translation(keyword=command_text.keyword, lang=lang);
    if not (redirect.group is None):
        remark = get_translation(keyword='redirect-remark', lang=lang);
        text = f'{message}: {redirect.group}\n\n{remark}';
    elif not (redirect.url is None):
        text = f'{message}: {redirect.url}';
    else:
        raise Exception('Command missing group/url attribute. Check config.');

    layout = get_message_options_basic(context.getReplyToMessage());
    return action_send_message(bot=bot, context=context, text=text, layout=layout, app_options=app_options);
