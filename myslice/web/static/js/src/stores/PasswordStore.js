import alt from '../alt';
import actions from '../actions/PasswordActions';
//import source from '../sources/PasswordSource';

class PasswordStore {

    constructor() {
        this.bindListeners({
            onSubmit: actions.ON_SUBMIT,

            updatePassword: actions.UPDATE_PASSWORD,
            updateHashing: actions.UPDATE_HASHING,
            errorupdatePassword: actions.ERRORUPDATE_PASSWORD,
            matchingPassword: actions.MATCHING_PASSWORD,
        });

        //this.registerAsync(source);
        
    }

    onSubmit() {
        console.log(this);
        //this.getInstance().onSubmit(state);
    }

    updatePassword (password) {
        this.setState({'password':password});
    }

    updateHashing (hashing) {
        this.setState({'hashing':hashing});
    }

    errorupdatePassword () {
        console.log('Error: passwords are not matching');
    }

    matchingPassword(){
        console.log("OK: Pasword is matching");
    }
}


export default alt.createStore(PasswordStore, 'PasswordStore');
