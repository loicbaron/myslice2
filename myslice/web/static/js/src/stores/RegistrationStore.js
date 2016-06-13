import alt from '../alt';
import actions from '../actions/RegistrationActions'
import source from '../sources/RegistrationSource'

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
            submitSuccess: actions.SUBMIT_SUCCESS,
            submitError: actions.SUBMIT_ERROR,
        });

        this.registerAsync(source);
    }

    updateAuthority(authority) {
        console.log(authority);
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

    submitSuccess(response) {

        this.message = response.data.error;
    }

    submitError(response) {

        this.message = response.data.error;
    }

}

export default alt.createStore(RegistrationStore, 'RegistrationStore');