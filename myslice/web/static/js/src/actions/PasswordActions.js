import alt from '../alt';

class PasswordActions {

    updateEmail(email) {
        return email;
    }
    errorupdateEmail() {
        return true;
    }
    submitEmail() {
        return true;
    }
    successEmail(){
        return true;
    }
}

export default alt.createActions(PasswordActions);
