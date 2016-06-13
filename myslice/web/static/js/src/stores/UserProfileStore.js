import alt from '../alt';
import UserProfileActions from '../actions/UserProfileActions';
import UserProfileSource from '../sources/ProfileSource';

class UserProfileStore {

    constructor() {
        this.email = '';
        this.first_name = '';
        this.last_name = '';
        this.authority = '';
        this.bio = "";
        this.url = "";
        this.errorMessage = null;
        this.loading = false;

        this.bindListeners({
            //changes views 
            updateFirstname: UserProfileActions.UPDATE_FIRSTNAME,
            updateLastname: UserProfileActions.UPDATE_LASTNAME,
            updateBio: UserProfileActions.UPDATE_BIO,
            updateUrl: UserProfileActions.UPDATE_URL,
            
            //async requests
            initUser: UserProfileActions.INIT_USER,
            onSubmit: UserProfileActions.ON_SUBMIT,
            updateLoading: UserProfileActions.UPDATE_LOADING,

            //update views from rest api results
            updateUser: UserProfileActions.UPDATE_USER,
            errorupdateUser: UserProfileActions.ERRORUPDATE_USER
        });
        
        this.registerAsync(UserProfileSource);
    }
    /*
    Initalize the user profile
    */
    initUser() {
        this.getInstance().initUser();
    }
    /*
    Submit updated user profile
    */
    onSubmit() {
        this.getInstance().onSubmit();
    }

    updateLoading(loading) {
        this.loading = loading;
    }

    updateUser(response) {
        this.setState(response.data.result);
    }

    errorupdateUser(errorMessage) {
        console.log(errorMessage);
    }

    updateFirstname(firstname) {
        this.first_name = firstname;
    }

    updateLastname(lastname) {
        this.last_name = lastname;
    }

    updateBio(bio) {
        this.bio = bio;
    }

    updateUrl(url) {
        this.url = url;
    }
}

export default alt.createStore(UserProfileStore, 'UserProfileStore');