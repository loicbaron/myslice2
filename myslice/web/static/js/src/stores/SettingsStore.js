import alt from '../alt';
import actions from '../actions/SettingsActions';
import source from '../sources/SettingsSource';

class SettingsStore {

    constructor() {
        //set profile as default pannel to see
        this.profile = {    "email"      : "",

                            "first_name" : "",
                            "last_name"  : "",
                            "authority"  : "",
                            "bio"        : "",
                            "url"        : "",
            }
        this.menuSelected = 'profile';
        this.oldPassword = '';
        this.newPassword = '';
        this.hashing = '';
        this.passwordUpdated = false;

        this.loading = false;

        this.bindListeners({
            updateLoading: actions.UPDATE_LOADING,
            updateSelected: actions.UPDATE_SELECTED,
            updateProfile: actions.UPDATE_PROFILE,

            fetchProfile: actions.FETCH_SETTINGS,
            submitProfile: actions.SUBMIT_PROFILE,
            generateKeys: actions.GENERATE_KEYS,
            submitPassword: actions.SUBMIT_PASSWORD,
            submitResetPassword: actions.SUBMIT_RESET_PASSWORD,
            
            updateOldpassword: actions.UPDATE_OLDPASSWORD,
            updateNewpassword: actions.UPDATE_NEWPASSWORD,
            updateHashing: actions.UPDATE_HASHING,

            updateSettings: actions.UPDATE_SETTINGS,
            errorupdateSettings: actions.ERRORUPDATE_SETTINGS,

            successUpdatePassword: actions.SUCCESS_UPDATE_PASSWORD,
            errorUpdatePassword: actions.ERROR_UPDATE_PASSWORD,
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

    submitResetPassword() {
        this.getInstance().submitResetPassword();
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

    updateOldpassword(oldPassword) {
        this.oldPassword = oldPassword;
    }

    updateNewpassword(newPassword) {
        this.newPassword = newPassword;
    }

    updateHashing (hashing) {
        this.hashing = hashing;
    }

    successUpdatePassword (response) {
        this.passwordUpdated = true;
    }

    errorUpdatePassword (error) {
        console.log(error);
    }
}


export default alt.createStore(SettingsStore, 'SettingsStore');
