process.env.NTBA_FIX_319 = 1;
/****************************************************************
 * IMPORTS
 ****************************************************************/

const DOTENV = require('dotenv')
DOTENV.config();
const { OPTIONS } = require('./src/setup/config.js');
const { MyApp } = require('./src/app.js');

/****************************************************************
 * METHODS
 ****************************************************************/

async function main () {
    console.log(`Setup app...`);
    const app = new MyApp(OPTIONS);
    app.setup();
    app.start();
    console.log(`Listening to user input...`);
}

/****************************************************************
 * EXECUTION
 ****************************************************************/

if (require.main === module) {
    main();
}
