import fs = require('fs');

export function fromFile(filename:string): any  {
        let secrets = JSON.parse(fs.readFileSync('secrets.json').toString())
        if (secrets.client_id === undefined) {
            throw new Error("missing client_id from secrets.json")
        }
        if (secrets.client_secret === undefined) {
            throw new Error("missing client_secret from secrets.json")
        }
        return secrets
}

