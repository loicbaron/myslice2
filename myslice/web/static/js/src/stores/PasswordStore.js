import alt from '../alt';
import actions from '../actions/PasswordActions';
import source from '../sources/PasswordSource';

class PasswordStore {

    constructor() {
        var password = '';
        var hashing = '';

        this.bindListeners({
            onSubmit: actions.ON_SUBMIT,

            updatePassword: actions.UPDATE_PASSWORD,
            updateHashing: actions.UPDATE_HASHING,
            errorupdatePassword: actions.ERRORUPDATE_PASSWORD,
            submitSuccess: actions.SUBMIT_SUCCESS,
            matchingPassword: actions.MATCHING_PASSWORD,
        });

        this.registerAsync(source);
        
    }

    onSubmit() {
        console.log(this);
        this.getInstance().onSubmit();
    }

    updatePassword (password) {
        this.password = password;
    }

    updateHashing (hashing) {
        this.hashing = hashing;
    }

    errorupdatePassword () {
        console.log('Error: passwords are not matching');
    }

    submitSuccess(){
        console.log("SUCCESS: password updated");
    }

    matchingPassword(){
        console.log("OK: Pasword is matching");
    }
}


export default alt.createStore(PasswordStore, 'PasswordStore');
