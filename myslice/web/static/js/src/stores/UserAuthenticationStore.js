import alt from '../alt';
import actions from '../actions/UserAuthenticationActions';
import profileaction from '../actions/UserProfileActions';
import source from '../sources/ProfileSource';

class UserAuthenticationStore {

    constructor() {
        this.message = '';
        this.public_key = '';
        this.private_key = '';

        this.bindListeners({
            fetchProfile: actions.FETCH_PROFILE,
            generateKeys: actions.GENERATE_KEYS,
            successMessage:actions.SUCCESS_MESSAGE,
            errorMessage: actions.ERROR_MESSAGE,

            updateUser: profileaction.UPDATE_USER,
        });

        this.registerAsync(source);
        
    }


    generateKeys() {
        this.getInstance().generateKeys();
    }

    fetchProfile () {
        this.getInstance().fetchProfile();
    }

    updateUser (response) {
        let user = response.data.result;
        this.setState({
            public_key:  user['public_key'],
            private_key: user['private_key']
        });
    }

    successMessage(){
        this.message = "SUCESS";
    }

    errorMessage() {
        this.message = "ERROR";
    }
}


export default alt.createStore(UserAuthenticationStore, 'UserAuthenticationStore');