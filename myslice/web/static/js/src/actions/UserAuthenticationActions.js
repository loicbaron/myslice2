import alt from '../alt';

class UserProfileActions {

    generateKeys() {
        return true;
    }

    successMessage(message) {
        return message;
    }

    errorMessage(message) {
        return message;
    }
}

export default alt.createActions(UserProfileActions);