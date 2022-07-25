process.env.NTBA_FIX_319 = 1;
/****************************************************************
 * IMPORTS
 ****************************************************************/

const DOTENV = require('dotenv')
DOTENV.config();
const { OPTIONS } = require('./src/setup/config.js');
const { Secrets } = require('./src/models/secrets');
const { MyApp } = require('./src/app.js');

/****************************************************************
 * METHODS
 ****************************************************************/

async function main () {
    console.log(`Setup app...`);
    let secret = new Secrets();
    const app = new MyApp(OPTIONS, secret);
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
