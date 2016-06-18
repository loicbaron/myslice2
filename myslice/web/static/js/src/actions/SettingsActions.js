import alt from '../alt';

class SettingsActions {

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

export default alt.createActions(SettingsActions);