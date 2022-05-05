# Technical notes #

Hier the design of the application and open issues are documented.

For contributes see [here](./CONTRIBUTING.md).

## Design of application ##

### Logical flow ###

The bot listens to all messages, then does the following
(see files in [src/behaviour/listeners](src/behaviour/listeners) for more):

- ignores posts by bots, regardless of content
- ignores too old messages, regardless of content
- if message has the syntactic form `@<botname> /?command [args...]`, then:
  - if command in config, then performs corresponding action;
  - else does nothing.
- if message has the syntactic form `/command @<botname>`, then:
  - if command in config, then performs corresponding action;
  - else does nothing.
- otherwise, does nothing.

### Posting language ###

The bot currently supports 5 languages and decides which language to use based on the following priorities (highest to lowest):

1. Language given as an argument by the admin when using `@<botname> cmd [args…]`, if provided.

2. Language hard coded into the [setup/config.yaml](setup/config.yaml) file for the command under `lang:`, if set.

3. Language of the message to which the admin replied to, if the call occurred this way.

4. ~~Language of the admin who called the command.~~

5. The default language set in [setup/config.yaml](setup/config.yaml) under `default-language:` (currently `uk` --- Ukrainian).

## Deployment ##

See [CONTRIBUTING.md](./CONTRIBUTING.md#deployment-and-logging).

## Notes and open issues ##

- It is unclear, whether the stopping proceedure for the bot is correct.
- Functionality of the bot is okay, but we should consider switching to `golang`,
  for which there is a well developed Telegram-API and which compiles, which in turn allows for cleaner development.
- Alternatively, there is are well structured `python` APIs (_python-telegram-bot_ + _telethon_),
  and in python one can at the very least artificially encode typing hints in all methods,
  allowing for cleaner development.
- Integration tests needed (currently developers are experimenting with possibilities here),
  in order to automatically test behaviour to increase the QA of each release
  and avoid »ärgerliche« bugs.
