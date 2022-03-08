# Contributions #

To separate source code, programme configurations, application data,
the respository is structured as follows:

```text
____. (root)
    |
    |____ /assets
    |    |_ ... # data e.g. translations
    |
    |____ /setup
    |    |_ ... # contains configuration of app
    |
    |____ /src
    |    |_ ... # source code
    |
    |____ /tests
    |    |_ ... # unit tests
    |
    |
    |_ .env         # not synchonised
    |_ Makefile     # need GNU make to use
    |_ package.json # need node and npm to use
```

In this file we document how developers can organise and contribute to the development of the application.

----

**Table of contents**

- [Contributions](#contributions)
  - [Workflow guidelines](#workflow-guidelines)
    - [Branches](#branches)
    - [Commits](#commits)
    - [Ticket Definition](#ticket-definition)
    - [Ticket in Doing](#ticket-in-doing)
    - [Ticket Review](#ticket-review)
    - [Ticket Merge-Strategie](#ticket-merge-strategie)
  - [Deployment and Logging](#deployment-and-logging)
    - [Deployment of live test bot](#deployment-of-live-test-bot)
    - [Deployment of live production bot](#deployment-of-live-production-bot)
    - [Logging](#logging)
  - [Development notes](#development-notes)
    - [Basic setup for developers](#basic-setup-for-developers)
    - [Develop new redirect command](#develop-new-redirect-command)
    - [Develop new special command](#develop-new-special-command)
  - [Testing notes](#testing-notes)
    - [Automatic testing](#automatic-testing)
    - [Local testing](#local-testing)
    - [Live tests](#live-tests)

----

## Workflow guidelines ##

Since the development of this application is a collaborative effort,
in order to keep development smoothly we would like to keep to the following guidlines.

### Branches ###

The relation between branches is as follows:
```text
-----------------------------------------> main
  \______> staging _________________/
     ||                         ||
     || all other branches:     ||
     ||                         ||
     ||__> dev-branch-unicorns__||
     |___> hotfix-error-404______|
       ...
```
where 'all else' includes **dev**, **hotfix**, and **bugfix** branches.

!!! The **main** branch and **staging** branches are hosted
and correspond to the live production and test applications respectively.

!!! So, unless absolutely trivial (and agreed upon), we should **never** push to main.

In each ticket a branch (off **staging**) should be created with a appropriate name according to the scheme:

- `dev-xxxx` where xxxx is in snake case, for ordinary development tickets
- `bug-xxxx` where xxxx is in snake case, for bug tickets.
- `hotfix-xxxx` where xxxx is in snake case, for hotfix tickets (thes are like bug tickets but have special priority).

### Commits ###

When committing please use the following scheme:
```text
{branch-from} > {branch-to}: {message}
```
Where:

- `{branch-from}` = name of branch
- `{branch-to}` = name of parent branch, to which the branch will be merged at the end of development.
  This is usually **staging**.
- `{message}` the commit message. This should contain a short description of what was done.
  Any longer descriptions should be added after a line break.

This **schema** makes reading lots of parallel changes in different branches easier to filter with the eye.

### Ticket Definition ###

1. Before ticket fully defined, keep it in 'backlog' with a `define me`-label
2. Add objectives as a _TODO_ checklist (acceptance criteria).
3. If the ticket is a Bug or Hotfix (= bug but with higher prio),
   add `[Bug]` or `[Hotfix]` to the start of the title.
4. Once ticket fully defined, remove the `define me`-label.

### Ticket in Doing ###

(provided ticket is fully defined and does not have `define me`-label)

1. Drag ticket from 'backlog' to 'doing' and assign your face to it.
2. Create a branch _from_ the staging branch according to the above scheme.
    </br>
    Note the name of the Branch in the ticket description.
3. When ticket completed (everything in _TODO_ list marked [x]):
    - create a pull request (branch ---> **staging**);
    - add a _How to Review_ checklist;
    - remove your face from ticket;
    - drag ticket into 'review'.

Please note the information in the [devlopment section](#development-notes) below.
It is also advisory to use [local testing](#local-testing) whilst developing.

### Ticket Review ###

(Tickets should only be reviewed by a different developer from the one in 'doing'.)

1. Assign your face to ticket.
2. Go through all the checks in the checklist (+ generally check that the general bot behaviour is not faulty).
    - If the review has open issues:
        1. if issue is large, add new points to _TODO_ and drag ticket into 'More work needed'.
        2. if issue small, clarify them with the original developer and then complete the below steps.
    - If the review is successful
        1. complete [merging](#ticket-merge-strategie);
        2. remove your face from ticket and drag to 'Done'.

See the [testing section](#testing-notes) below for information about local/live testing.

### Ticket Merge-Strategie ###

!!! Never merge directly to **main** branch !!!

Order is **ticket branch** ---> **staging** ---> **main**.

1. Change the Version in [dist/Version](dist/Version) and [package.json](package.json).
    Run `make clean && make build`, to update [package-lock.json](package-lock.json).
2. Commit this change, and accept the PR.
   </br>
   You may delete the branch when done
   </br>
   (but _do not_ delete **staging**!).
   </br>
   Ensure that live test instance of the app has been successfully [deployed](#deployment-of-live-test-bot).
3. _Only if_ we want to release the changes properly, create a PR **staging ---> main**.
    </br>
    (This should automatically be the case for hotfixes.)
    </br>
    Perform [live tests](#live-tests) on the instance of the application before accepting this PR.
    </br>
    **Do NOT** delete the staging branch!
    </br>
    Ensure that live production instance of the app has been successfully [deployed](#deployment-of-live-production-bot).

## Deployment and Logging ##

### Deployment of live test bot ###

- Log in to our deployment tool.
- Select the app **leipzig-helps-ukraine** (staging).
- Check the latest activity. If the app is not running:
  - open the _Deploy_ tab
  - select 'staging' in both automatic and manual deployment
  - deploy the branch.

Also check the logs (see below).

### Deployment of live production bot ###

- Log in to our deployment tool.
- Select the app **leipzig-helps-ukraine** (production).
- Check the latest activity. If the app is not running:
  - open the _Deploy_ tab
  - select 'staging' in both automatic and manual deployment
  - deploy the branch.

Also check the logs (see below).

### Logging ###

In the deployment tool select _Overview_ then select the logging add-on.

----

## Development notes ##

We document here how to set up and provide hints regarding the development of simple changes.

### Basic setup for developers ###

Create a `.env` file with (at least) the following contents:
```.env
token={your API Token}
```

- You may need to update your version of _npm_/_node_.
- To compile and test the application,
  use the `npm run build` and `npm run start` (or `make build` and `make run`) commands.
  (See also [local testing](#local-testing).)
- For a fresh start, call `make clean` to delete all artefacts.

### Develop new redirect command ###

To add a new redirect button, the following parts have to be changed:

- [setup/config.yaml](setup/config.yaml) -> add a command
  (cf. commands like `/transport`, `/housing`, _etc._).
- [assets/language.yaml](assets/language.yaml) -> if necessary add translations for new keyword.

And that's it! No need to add any code!

### Develop new special command ###

To add a new special command (amongst `/start`, `/help`, `/pin`, _etc._),
the following parts have to be changed:

- [setup/config.yaml](setup/config.yaml) -> add a command.
- [assets/language.yaml](assets/language.yaml) -> if necessary add translations for new keyword.
- [src/parts/actions.js](src/parts/actions.js) -> „ergänze“ `universal_action` to cater for new case.
  </br>
  One can also if necessary follow the logic backwards from there (`actions.js` <- `listeners.js` <- `app.js`),
  and adjust things that happen 'higher up'.

## Testing notes ##

Currently this is parcelled out into automatic tests, local testing, live testing.

### Automatic testing ###

Call
```bash
make tests
```
or
```bash
npm run test
```

to run the unit tests.

Live integration tests to be added.
To use, the bot will have to be started before calling the above commands.

### Local testing ###

Tickets should always be tested locally first.

Do this once:

- Speak to `@BotFather` and create your own bot (just for you) if you have not already done so.
- Ask `@BotFather` for the bot's API token, and add it to your **.env** file as follows
    ```bash
    ## this is my local bot's api token. I should not share this with anybody!
    token=01234567:ABCDefg_1289dU138 # <- this is just an example obvs!
    ```
- Create a group just for you and `@<name-of-local-test-bot>`.
  </br>
  Ensure you and `@<name-of-local-test-bot>` have admin status.
  </br>
  The `@<name-of-local-test-bot>` only needs rights to delete messages.

To test:

- Start the bot:
    ```bash
    make clean # <- optional
    make build # <- only needed if code or config or assets have changed
    make run
    ```
- Enter the chat group and interact with the bot.

For more explicit logging, set
```yaml
options:
  debug: true
  full-censor-user: false # optional
```
in the [config.yaml](setup/config.yaml) file and restart the bot.
</br>
With this option, logging takes place upon every message,
instead of just relevant messages as per default.

### Live tests ###

If the **staging** branch has been changed, the live test bot should be tested!

Do this once:

- Create a group just for you and `@<name-of-live-test-bot>`.
- Ensure you and `@<name-of-live-test-bot>` have admin status.
- `@<name-of-live-test-bot>` only needs rights to delete messages

To test:

- Enter the chat group and interact with the bot.
