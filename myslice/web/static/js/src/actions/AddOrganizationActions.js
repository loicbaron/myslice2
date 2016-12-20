/**
 * Created by amirabradai on 01/12/2016.
 */
import alt from '../alt';

class AddOrganizationActions {

    updateEmail(email) {
        return email;
    }
    updateSiteweb(siteweb) {
        return siteweb;
    }
    updateAName(aname) {
        return aname;
    }

    updatePassword(password) {
        console.log("action pass");
        return password;
    }

    updateFirstname(first_name) {
        return first_name;
    }

    updateLastname(last_name) {
        return last_name;
    }

    updateTerms(terms) {
        return terms;
    }

    loading(loading) {
        return loading;
    }

    submitForm() {
        this.loading(true);
        return true;
    }

    submitSuccess(response) {
        this.loading(false);
        return response;
    }

    submitError(response) {
        this.loading(false);
        return response;
    }
    submitAuthoritySuccess(response) {
        this.loading(false);
        return response;
    }

    submitAuthorityError(response) {
        this.loading(false);
        return response;
    }

}

export default alt.createActions(AddOrganizationActions);