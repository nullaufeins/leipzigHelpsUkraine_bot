# Telegram Bot - **@LeipzigHelpsUkraine** #

## Usage ##

**Please enter `/` in the message input box of the telegram group to choose the command from a selection. This will prevent typo errors!**

Admins have access to the following commands:

- Special commands:
  - `/help`    - displays main menu (in the language of the admin using the command)
  - `/pin` - displays **and pins** main menu in group.
    There are the following variants:

    | Variant    | Output language of post |
    | :--------- | :---------------------- |
    | `/pin`     | Defaults to English     |
    | `/pin_de`  | German                  |
    | `/pin_uk`  | Ukrainian               |

- Redirect commands:
  - Quick link to telegram-subgroups:
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
  - `/homepage` - browser link to webpage.
  - `/feedback` - telegram-link to sub group for technical feedback for bot.

### Advanced ###

For greater control, admins may also send commands with arguments directly to the bot via:

```md
@<botname> command [args...]
```

The following commands + optional args are available.

| Command                        | Behaviour                                                 |
| :----------------------------- | :-------------------------------------------------------- |
| `@<botname> pin [xx]`          | Pin command (default English, otherwise in language xx)   |
| `@<botname> pin all`           | Pin command - posts menu in all languages and pins 1st    |
| `@<botname> help [xx]`         | Pin command - posts menu in all languages and pins 1st    |
| `@<botname> transport [xx]`    | Quick link to subgroup (default in en, else language xx). |
| `@<botname> housing [xx]`      | " |
| `@<botname> translations [xx]` | " |
| `@<botname> legal [xx]`        | " |
| `@<botname> donations [xx]`    | " |
| `@<botname> homepage [xx]`     | Posts link to webpage (default in en, else language xx).  |
| `@<botname> feedback [xx]`     | Quick link to to subgroup for feedback.                   |

Here, `[...]` means that the argument is optional,
</br>
and `xx` can be any of the following language codes:

| Code  | Language   |
| :---- | :--------- |
| `en`  | English    |
| `pl`  | Polish     |
| `ru`  | Russian    |
| `uk`  | Ukrainian  |

_e.g._

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

## Development ##

See [here](./README-TECHNICAL.md).
