import alt from '../alt';
import actions from '../actions/RegistrationActions'
import source from '../sources/RegistrationSource'

class RegistrationStore {

    constructor() {
        this.authority = '';
        this.email = '';
        this.first_name = '';
        this.last_name = '';
        this.loading = false;
        this.success = false;
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

    updateFirstname(first_name) {
        this.first_name = first_name;
    }

    updateLastname(last_name) {
        this.last_name = last_name;
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
        this.success = true;
    }

    submitError(response) {
        this.errorMessage = response.data.error;
    }

}

export default alt.createStore(RegistrationStore, 'RegistrationStore');
