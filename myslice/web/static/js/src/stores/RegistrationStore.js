var alt = require('../alt');
var actions = require('../actions/RegistrationActions');

class RegistrationStore {

    constructor() {
        this.authority = '';
        this.email = '';
        this.firstname = '';
        this.lastname = '';
        this.errorMessage = null;

        this.bindListeners({
            updateAuthority: actions.UPDATE_AUTHORITY,
            updateEmail: actions.UPDATE_EMAIL,
            updateFirstname: actions.UPDATE_FIRSTNAME,
            updateLastname: actions.UPDATE_LASTNAME,

        });
    }

    updateAuthority(authority) {
        this.authority = authority;
    }

    updateEmail(email) {
        this.email = email;
    }

    updateFirstname(firstname) {
        this.firstname = firstname;
    }

    updateLastname(lastname) {
        this.lastname = lastname;
    }

}

module.exports = alt.createStore(RegistrationStore, 'RegistrationStore');