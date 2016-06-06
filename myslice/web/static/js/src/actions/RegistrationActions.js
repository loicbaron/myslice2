var alt = require('../alt');

class RegistrationActions {

    updateAuthority(authority) {
        return authority;
    }

    updateEmail(email) {
        return email;
    }

    updateFirstname(firstname) {
        return firstname;
    }

    updateLastname(lastname) {
        return lastname;
    }
}

module.exports = alt.createActions(RegistrationActions);