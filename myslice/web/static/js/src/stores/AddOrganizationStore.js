/**
 * Created by amirabradai on 01/12/2016.
 */

import alt from '../alt';
import source from '../sources/AddOrganizationSource';
import actions from '../actions/AddOrganizationActions';

class AddOrganizationStore {

constructor() {
        this.aname='';
        this.email = '';
        this.authority= '';
        this.password = '';
        this.first_name = '';
        this.siteweb = '';
        this.shortname='';

        this.domains=[ ];
        this.last_name = '';
        this.short_name = '';
        this.terms = false;
        this.loading = false;
        this.success = false;
        this.errorMessage = null;
        this.bindListeners({

            updateEmail: actions.UPDATE_EMAIL,
            updatePassword: actions.UPDATE_PASSWORD,
            updateFirstname: actions.UPDATE_FIRSTNAME,
            updateSiteweb: actions.UPDATE_SITEWEB,
            updateAName: actions.UPDATE_ANAME,
            updateLastname: actions.UPDATE_LASTNAME,
            updateTerms: actions.UPDATE_TERMS,
            updateLoading: actions.LOADING,
            submitForm: actions.SUBMIT_FORM,
            submitAuthoritySuccess: actions.SUBMIT_AUTHORITY_SUCCESS,
            submitAuthorityError: actions.SUBMIT_AUTHORITY_ERROR,
        });

        this.registerAsync(source);
    }



    updateEmail(email) {
        console.log("update email = "+email);
        this.email = email;
    }
    updateSiteweb(siteweb) {

        this.siteweb = siteweb;
    }

    updateAName(aname) {

        this.aname = aname;
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
            this.getInstance().submitAuthority();
        }
    }

    submitAuthoritySuccess(response) {
        this.success = true;
    }

    submitAuthorityError(response) {
        this.errorMessage = response.data.error;
    }





}


export default alt.createStore(AddOrganizationStore, 'AddOrganizationStore');