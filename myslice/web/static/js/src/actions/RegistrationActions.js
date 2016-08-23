import alt from '../alt';

class RegistrationActions {

    updateAuthority(authority) {
        return authority;
    }

    updateEmail(email) {
        return email;
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
}

export default alt.createActions(RegistrationActions);
