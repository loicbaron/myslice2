import alt from '../alt';
import actions from '../actions/PasswordActions';
import source from '../sources/PasswordSource';

class PasswordStore {

    constructor() {
        var email = '';
        var password = '';
        var hashing = '';
        var matching = true;
        var sent = false;
        var updated = false;

        this.bindListeners({
            onSubmit: actions.ON_SUBMIT,
            submitEmail: actions.SUBMIT_EMAIL,

            updatePassword: actions.UPDATE_PASSWORD,
            updateEmail: actions.UPDATE_EMAIL,
            updateHashing: actions.UPDATE_HASHING,
            errorupdatePassword: actions.ERRORUPDATE_PASSWORD,
            errorupdateEmail: actions.ERRORUPDATE_EMAIL,
            submitSuccess: actions.SUBMIT_SUCCESS,
            successEmail: actions.SUCCESS_EMAIL,
            matchingPassword: actions.MATCHING_PASSWORD,
        });

        this.registerAsync(source);
        
    }

    onSubmit() {
        if(this.matching){
            this.getInstance().onSubmit();
        }
    }
    submitEmail() {
        this.getInstance().submitEmail();
    }
    updatePassword (password) {
        this.password = password;
    }
    updateEmail (email) {
        this.email = email;
    }
    updateHashing (hashing) {
        this.hashing = hashing;
    }

    errorupdatePassword () {
        console.log('Error: passwords are not matching');
        this.matching = false;
    }
    errorupdateEmail () {
        console.log('Error: invalid email');
    }
    submitSuccess(){
        console.log("SUCCESS: password updated");
        this.updated = true;
    }
    successEmail(){
        console.log("SUCCESS: an email has been sent");
        this.sent = true;
    }
    matchingPassword(){
        console.log("OK: Pasword is matching");
        this.matching = true;
    }
}


export default alt.createStore(PasswordStore, 'PasswordStore');
