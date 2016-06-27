import alt from '../alt';

class PasswordActions {

    updatePassword(password) {
        return password;
    }
    updateEmail(email) {
        return email;
    }
    updateHashing(hashing) {
        return hashing;
    }

    errorupdatePassword() {
        return true;
    }
    errorupdateEmail() {
        return true;
    }
    matchingPassword() {
        return true;
    }

    onSubmit() {
        return true;
    }
    submitEmail() {
        return true;
    }
    submitSuccess() {
        return true;
    }
    successEmail(){
        return true;
    }
}

export default alt.createActions(PasswordActions);
