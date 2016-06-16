import alt from '../alt';
import actions from '../actions/UserAuthenticationActions';
import source from '../sources/ProfileSource';

class AuthoritiesStore {

    constructor() {
        this.message = '';
        this.pk = {
            mime: 'text/plain',
            filename: 'myexportedfile.txt',
            contents: 'all of the exports',
        }

        this.bindListeners({
            generateKeys: actions.GENERATE_KEYS,
            successMessage:actions.SUCCESS_MESSAGE,
            errorMessage: actions.ERROR_MESSAGE,
        });

        this.registerAsync(source);
        
    }


    generateKeys() {
        this.getInstance().generateKeys();
    }

    successMessage(){
        this.message = "SUCESS";
    }

    errorMessage() {
        this.message = "ERROR";
    }
}


export default alt.createStore(AuthoritiesStore, 'AuthoritiesStore');