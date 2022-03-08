# Telegram Bot - **@LeipzigHelpsUkraine** #

## Usage ##

**Enter "`/`" in the message input-box of the telegram group, then choose the `/command` from the suggestions.** This prevents typing errors!

Admins have access to the following commands:

- `/help`    - displays main menu (in the language of the admin using the command)
- The following commands post a telegram-link to subgroups:
  ```
  /animals
  /arrival
  /donations
  /family
  /housing
  /legal
  /translations
  /transport
  ```
- `/homepage` - posts a browser link to webpage.
- `/feedback` - posts a telegram-link to a subgroup for technical feedback for bot.
- `/pin` - displays **and pins** main menu in group.
  There are the following variants:

  | Variant    | Output language of post |
  | :--------- | :---------------------- |
  | `/pin`     | Defaults to German      |
  | `/pin_en`  | English                 |
  | `/pin_uk`  | Ukrainian               |

### Advanced ###

For greater control, admins may also send commands with arguments directly to the bot via:

```md
@<botname> command [args...]
```

**Enter "`@`" in the message input-box of the telegram group, then select the `@<bot-name>` to autocomplete the first part,** then type in the `command [args...]` part.
</br>
The following table provides a list of the possibilities:

| Command             | Behaviour    |
| :------------------ | :----------- |
| `help [xx]`         | Posts menu in language `xx`^ |
| `animals [xx]`      | Posts link to telegram subgroup in language `xx`^ |
| `arrival [xx]`      | " |
| `donations [xx]`    | " |
| `family [xx]`       | " |
| `housing [xx]`      | " |
| `legal [xx]`        | " |
| `translations [xx]` | " |
| `transport [xx]`    | " |
| `homepage [xx]`     | Posts link to webpage in language `xx`^  |
| `feedback [xx]`     | Posts link to subgroup for feedback in language `xx`^ |
| `pin [xx]`          | Pin command in language `xx`^ |
| `pin all`           | Pin command - posts menu in all languages and pins 1st |

Notes:
- Here, `[...]` means that the argument is optional
- `xx` can be any of the following language codes:

    | Code  | Language   |
    | :---- | :--------- |
    | `de`  | German     |
    | `en`  | English    |
    | `pl`  | Polish     |
    | `ru`  | Russian    |
    | `uk`  | Ukrainian  |
- `^` the language in which the bot posts is decided by the following priorities:
  - language `xx` if given;
  - otherwise: language of message replied to, if the admin replied to a message;
  - otherwise: the default language (German).

For example

```md
@<botname> help pl
@<botname> legal uk
```

prints the help menu in Polish, shows the redirect link to legal issues in Ukrainian,
_etc._ regardless of the user's language setting.

## Help! How do I ... ? ##

### Shut down the bot ###

To shut down the bot, the easiest way is to remove it from the telegram group.

(It can always be added again at a later stage.)

## Technical information for developers ##

See [technical notes](./TECHNICAL.md) and [contributions](./CONTRIBUTING.md).
