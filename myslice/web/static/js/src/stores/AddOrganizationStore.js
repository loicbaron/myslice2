/**
 * Created by amirabradai on 01/12/2016.
 */

import alt from '../alt';
import actions from '../actions/AddOrganizationActions';

class AddOrganizationStore {

constructor() {
        this.authority = '';
        this.email = '';
        this.password = '';
        this.first_name = '';
        this.last_name = '';
        this.terms = false;
        this.loading = false;
        this.success = false;
        this.errorMessage = null;
        this.bindListeners({

            updateEmail: actions.UPDATE_EMAIL,
            updatePassword: actions.UPDATE_PASSWORD,
            updateFirstname: actions.UPDATE_FIRSTNAME,
            updateLastname: actions.UPDATE_LASTNAME,
            updateTerms: actions.UPDATE_TERMS,
            updateLoading: actions.LOADING,
            submitForm: actions.SUBMIT_FORM,
            submitSuccess: actions.SUBMIT_SUCCESS,
            submitError: actions.SUBMIT_ERROR,
        });

      //  this.registerAsync(source);
    }



    updateEmail(email) {
        console.log("update email = "+email);
        this.email = email;
    }
    updatePassword(password) {
        console.log("update password");
        this.password = password;
    }
    updateFirstname(first_name) {
        console.log("update firstname = "+first_name);
        this.first_name = first_name;
    }

    updateLastname(last_name) {
        console.log("update lastname = "+last_name);
        this.last_name = last_name;
    }

    updateTerms(terms) {
        this.terms = terms;
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


export default alt.createStore(AddOrganizationStore, 'AddOrganizationStore');