import alt from '../alt';
import actions from '../actions/ProfileActions';
import source from '../sources/SettingsSource';

class ProfileStore {

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
            updateFirstname: actions.UPDATE_FIRSTNAME,
            updateLastname: actions.UPDATE_LASTNAME,
            updateBio: actions.UPDATE_BIO,
            updateUrl: actions.UPDATE_URL,
            
            //async requests
            fetchProfile: actions.FETCH_PROFILE,
            onSubmit: actions.ON_SUBMIT,
            updateLoading: actions.UPDATE_LOADING,

            //update views from rest api results
            updateUser: actions.UPDATE_USER,
            errorupdateUser: actions.ERRORUPDATE_USER
        });
        
        this.registerAsync(source);
    }
    /*
    Initalize the user profile
    */
    fetchProfile() {
        this.getInstance().fetchProfile();
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

export default alt.createStore(ProfileStore, 'ProfileStore');