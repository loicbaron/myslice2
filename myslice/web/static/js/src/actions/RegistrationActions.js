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

    loading(loading) {
        return loading;
    }

    submitForm() {
        this.loading(true);
        return true;
    }
}

module.exports = alt.createActions(RegistrationActions);