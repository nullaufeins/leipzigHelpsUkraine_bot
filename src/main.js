process.env.NTBA_FIX_319 = 1;
/****************************************************************
 * IMPORTS
 ****************************************************************/

const DOTENV = require('dotenv')
DOTENV.config();
const { OPTIONS } = require.main.require('./setup/config.js');
const { MyApp } = require.main.require('./application/app.js');

/****************************************************************
 * METHODS
 ****************************************************************/

async function main () {
    console.log(`Running \x1b[1m${process.env.app}\x1b[1m.`);
    console.log(`Setup app...`);
    const app = new MyApp(OPTIONS);
    app.setup();
    console.log(`Listening to user input...`);
}

/****************************************************************
 * EXECUTION
 ****************************************************************/

if (require.main === module) {
    main();
}
