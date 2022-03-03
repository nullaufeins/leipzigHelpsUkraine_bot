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
    /transport
    /housing
    /translations
    /legal
    /donations
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
## Shutdown bot ##

To shut down the bot, the easiest way is to remove it from the telegram group.

(It can always be added again at a later stage.)

## Setup ##

Set up `.env` as

```.env
token={your API Token}
```

call

```bash
npm upgrade
npm run start
```

or simply:

```bash
make build # only need to do this when dependencies are changed
make run
```

to setup and run.

For a fresh start, call `make clean` to delete all artefacts.

## Contributions ##

The internal logic of the app has been refactored, in order to cleanly separate:

- source code;
- programme configurations;
- application data.

Most feature changes can be performed by simply editing
  [`./src/settings/config.yaml`](src/settings/config.yaml)
  and
  [`./assets/language.yaml`](assets/language.yaml)
for the config and data respectively.
_Only_ if a behavioural change is required, does one need to change the code,
and it very likely would suffice to just change the logic in the `universal_action` function
(or add a subfunction) in [`./src/parts/actions.yaml`](src/parts/actions.yaml).

### Contribute new redirect ###

To add a new redirect button, the following parts have to be changed:

- [./src/setup/config.yaml](src/setup/config.yaml) -> add a command
  (cf. commands like `/transport`, `/housing`, _etc._).
- [./assets/language.yaml](assets/language.yaml) -> if necessary add translations for new keyword.

And that's it! No need to add any code!

### Contribute new special command ###

To add a new special command (amongst `/start`, `/help`, `/pin`, _etc._),
the following parts have to be changed:

- [./src/setup/config.yaml](src/setup/config.yaml) -> add a command.
- [./assets/language.yaml](assets/language.yaml) -> if necessary add translations for new keyword.
- [./src/parts/actions.js](src/parts/actions.js) -> „ergänze“ `universal_action` to cater for new case.
  </br>One can also if necessary follow the logic backwards from there (`actions.js` <- `listeners.js` <- `app.js`), and adjust things that happen 'higher up'.

## Notes and issues ##

- To restart the bot, change something trivial _e.g._ in `package.json` or a `.js` file (add and remove a space or something trivial),
  then save.
- Whilst ErrorCatching seems to cause no issues, we should add some.
- Stopping the bot produces an error. It would be nice to have the bot stop in a controlled manner
  (see [`./src/app.js`](src/app.js)).
