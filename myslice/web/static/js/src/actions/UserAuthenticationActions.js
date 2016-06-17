import alt from '../alt';

class UserAuthenticationActions {

    generateKeys() {
        return true;
    }

    successMessage(message) {
        return message;
    }

    errorMessage(message) {
        return message;
    }

    fetchProfile() {
        return true;
    }

    updateUser(response) {
        console.log('sss')
        return response;
    }

}

export default alt.createActions(UserAuthenticationActions);