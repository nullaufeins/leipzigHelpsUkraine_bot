# Integration tests #

These instructions are based on <https://core.telegram.org/api/obtaining_api_id>.

1. Open <https://my.telegram.org/> and log in as yourself.
2. Click on [API development tools](https://my.telegram.org/apps) and create a test app.
3. Copy the `app_id` and `app_hash` tokens.
4. Create an **.env** file in the _root directory_ of the project (_only on your local cloned copy!_).
5. Paste in the copied information into the **.env** file (_cf._ example template in [templates/.env](../templates/.env)).

**NOTE:**
- Do not abuse the registered account (_i.e._ usage beyond mere testing),
  or Telegram will permanently ban your user account.
- Telegram monitors usage of their API, so avoid usage of personal information (real names, addresses, _etc._).
- So, keep the tests simple. We just want to check that our simple bot-app behaves as intended.

## Execution of integration tests ##

Ensure that all the requirements are met. If not, call `just build`.

To run integration tests, open two bash terminals.

- In one, call `just run`. This will start app and keep it alive.
- In the other call `just tests-integration` (or `just tests` which runs the unit tests too).

Alternatively, one can call
```bash
just run &
just tests-integration
```
which keeps the app alive and runs the integration tests.

A further alternative is to use the docker framework.
Start docker and then call
```bash
just docker-itests
```

**Note:** By the first attempt, you will be asked to verify with a code sent to the telegram app.
Provided the session files are not deleted, you will not have to repeat this.

## How it works ##

We rely heavily on the following packages:

- pyrogram
- tgintegration

The `pyrogram` module provides the basic tools to create a client.
The `tgintegration` module provides further advanced tools.
