# Development notes #

To set up and contribute please read the following sections.

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
  [`./setup/config.yaml`](setup/config.yaml)
  and
  [`./assets/language.yaml`](assets/language.yaml)
for the config and data respectively.
_Only_ if a behavioural change is required, does one need to change the code,
and it very likely would suffice to just change the logic in the `universal_action` function
(or add a subfunction) in [`./src/parts/actions.yaml`](src/parts/actions.yaml).

### Contribute new redirect ###

To add a new redirect button, the following parts have to be changed:

- [./setup/config.yaml](setup/config.yaml) -> add a command
  (cf. commands like `/transport`, `/housing`, _etc._).
- [./assets/language.yaml](assets/language.yaml) -> if necessary add translations for new keyword.

And that's it! No need to add any code!

### Contribute new special command ###

To add a new special command (amongst `/start`, `/help`, `/pin`, _etc._),
the following parts have to be changed:

- [./setup/config.yaml](setup/config.yaml) -> add a command.
- [./assets/language.yaml](assets/language.yaml) -> if necessary add translations for new keyword.
- [./src/parts/actions.js](src/parts/actions.js) -> „ergänze“ `universal_action` to cater for new case.
  </br>One can also if necessary follow the logic backwards from there (`actions.js` <- `listeners.js` <- `app.js`), and adjust things that happen 'higher up'.

## Notes and issues ##

- To restart the bot, change something trivial _e.g._ in `package.json` or a `.js` file (add and remove a space or something trivial),
  then save.
- Whilst ErrorCatching seems to cause no issues, we should add some.
- Stopping the bot produces an error. It would be nice to have the bot stop in a controlled manner
  (see [`./src/app.js`](src/app.js)).

## Testing and Deployment ##

Currently this is parcelled out into local testing,
live testing, and production release.

## Logical flow ##

The bot listens to all messages, then does the following
(see [./src/parts/listeners.js](src/parts/listeners.js) for more):

- ignores posts by bots, regardless of content
- ignores too old messages, regardless of content
- if message has the syntactic form `@<botname> /?command [args...]`, then:
  - if command in config, then performs corresponding action;
  - else does nothing.
- if message has the syntactic form `/command @<botname>`, then:
  - if command in config, then performs corresponding action;
  - else does nothing.
- otherwise, does nothing.
