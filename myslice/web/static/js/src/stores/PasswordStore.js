import alt from '../alt';
import actions from '../actions/PasswordActions';
import source from '../sources/PasswordSource';

class PasswordStore {

    constructor() {
        var email = '';
        var sent = false;

        this.bindListeners({
            submitEmail: actions.SUBMIT_EMAIL,

            updateEmail: actions.UPDATE_EMAIL,
            errorupdateEmail: actions.ERRORUPDATE_EMAIL,
            successEmail: actions.SUCCESS_EMAIL,
        });

        this.registerAsync(source);
        
    }

    submitEmail() {
        this.getInstance().submitEmail();
    }
    updateEmail (email) {
        this.email = email;
    }

    errorupdateEmail () {
        console.log('Error: invalid email');
    }
    successEmail(){
        console.log("SUCCESS: an email has been sent");
        this.sent = true;
    }
}


export default alt.createStore(PasswordStore, 'PasswordStore');
