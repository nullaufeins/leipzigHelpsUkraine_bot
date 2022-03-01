# Telegram Bot - Weiterleitung für Freiwillige #

Set up `.env` as

```.env
token={your API Token}
```

call

```bash
npm upgrade
node src/main.js
```

or simply:

```bash
make build # only need to do this once, unless there have been code changes.
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

## Notes ##

- Messages from users to the bot, which are recognised as commands are auto deleted after a set time.
  </br>
  (All other messages are retained.)
  </br>
  Set the lengths of these timeouts in [`./src/settings/config.yaml`](src/settings/config.yaml).
