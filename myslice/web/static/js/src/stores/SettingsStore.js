import alt from '../alt';
import actions from '../actions/SettingsActions';
import source from '../sources/SettingsSource';

class SettingsStore {

    constructor() {
        //set profile as default pannel to see
        this.settings = null;
        this.menuSelected = 'profile';
        this.newPassword = '';

        this.loading = false;

        this.bindListeners({
            updateLoading: actions.UPDATE_LOADING,
            updateSelected: actions.UPDATE_SELECTED,

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

    submitProfile(childstate) {
        this.getInstance().submitProfile(childstate);
    }

    generateKeys() {
        this.getInstance().generateKeys();
    }

    updateSettings (response) {
        this.setState({ settings: response.data.result});
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

    repeatPassword(oldPassword) {
        this.settings.password = oldPassword;
    }

    resetPassword(newPassword) {
        this.newPassword = newPassword;
    }

    submitPassword() {
        this.getInstance().submitPassword();
    }

}


export default alt.createStore(SettingsStore, 'SettingsStore');