/****************************************************************
 * IMPORTS
 ****************************************************************/

//

/****************************************************************
 * Class Secrets
 ****************************************************************/

class Secrets {
    constructor() {
        this.token = process.env.TOKEN;
    }
}

/****************************************************************
 * EXPORTS
 ****************************************************************/

module.exports = {
    Secrets
};
