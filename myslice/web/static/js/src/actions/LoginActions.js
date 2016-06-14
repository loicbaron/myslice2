var alt = require('../alt');

class LoginActions {

    updateEmail(email) {
        return email;
    }

    updatePassword(password) {
        return password;
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

export default alt.createActions(LoginActions);