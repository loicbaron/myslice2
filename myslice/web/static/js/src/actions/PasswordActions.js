import alt from '../alt';

class PasswordActions {

    updatePassword(password) {
        return password;
    }

    updateHashing(hashing) {
        return hashing;
    }

    errorupdatePassword() {
        return true;
    }

    matchingPassword() {
        return true;
    }

    onSubmit() {
        return true;
    }

}

export default alt.createActions(PasswordActions);
