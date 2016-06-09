var alt = require('../alt');
var actions = require('../actions/RegistrationActions');
var source = require('../sources/RegistrationSource');

class RegistrationStore {

    constructor() {
        this.authority = '';
        this.email = '';
        this.firstname = '';
        this.lastname = '';
        this.loading = false;
        this.errorMessage = null;

        this.bindListeners({
            updateAuthority: actions.UPDATE_AUTHORITY,
            updateEmail: actions.UPDATE_EMAIL,
            updateFirstname: actions.UPDATE_FIRSTNAME,
            updateLastname: actions.UPDATE_LASTNAME,
            updateLoading: actions.LOADING,
            submitForm: actions.SUBMIT_FORM,
        });

        this.registerAsync(source);
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

    updateLoading(loading) {
        this.loading = loading;
    }

    submitForm() {

        if (!this.getInstance().isLoading()) {
            this.getInstance().submit();
        }
    }

}

module.exports = alt.createStore(RegistrationStore, 'RegistrationStore');