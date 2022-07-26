/****************************************************************
 * IMPORTS
 ****************************************************************/

const { Message } = require('./message.js');

/****************************************************************
 * Class Trace for debugging only!
 ****************************************************************/

class Trace {
    constructor() {
        this.path = [];
    }

    add(x) { this.path.push(x); }

    toRepr() { return this.path.join(' -> '); }

    toString() { return this.toRepr(); }
}

/****************************************************************
 * EXPORTS
 ****************************************************************/

module.exports = {
    Trace
};