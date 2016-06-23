import alt from '../alt';
import actions from '../actions/SettingsActions';
import source from '../sources/SettingsSource';

class SettingsStore {

    constructor() {
        //set profile as default pannel to see
        this.profile = {   "email"      : "",

                            "first_name" : "",
                            "last_name"  : "",
                            "authority"  : "",
                            "bio"        : "",
                            "url"        : "",
            }
        this.menuSelected = 'profile';
        this.newPassword = '';

        this.loading = false;

        this.bindListeners({
            updateLoading: actions.UPDATE_LOADING,
            updateSelected: actions.UPDATE_SELECTED,
            updateProfile: actions.UPDATE_PROFILE,

            fetchProfile: actions.FETCH_SETTINGS,
            submitProfile: actions.SUBMIT_PROFILE,
            generateKeys: actions.GENERATE_KEYS,
            submitPassword: actions.SUBMIT_PASSWORD,
            
            repeatPassword: actions.REPEAT_PASSWORD,
            resetPassword: actions.RESET_PASSWORD,

            updateSettings: actions.UPDATE_SETTINGS,
            errorupdateSettings: actions.ERRORUPDATE_SETTINGS,
        });

        this.registerAsync(source);
        
    }

    fetchProfile () {
        this.getInstance().fetchSettings();
    }

    submitProfile() {
        this.getInstance().submitProfile();
    }

    submitPassword() {
        this.getInstance().submitPassword();
    }

    generateKeys() {
        this.getInstance().generateKeys();
    }

    updateSettings (response) {
        this.setState({ profile: response.data.result});
    }

    errorupdateSettings (error) {
        console.log(error);
    }

    updateLoading(loading) {
        this.loading = loading;
    }

    updateSelected(name) {
        this.menuSelected = name;
    }

    updateProfile(array) {
        this.profile[array[0]] = array[1];
    }

    repeatPassword(oldPassword) {
        this.profile.password = oldPassword;
    }

    resetPassword(newPassword) {
        this.newPassword = newPassword;
    }



}


export default alt.createStore(SettingsStore, 'SettingsStore');