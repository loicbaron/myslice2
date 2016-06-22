import alt from '../alt';
import actions from '../actions/SettingsActions';
import source from '../sources/SettingsSource';

class SettingsStore {

    constructor() {
        //set profile as default pannel to see
        this.settings = null;
        this.menuSelected = 'profile';

        this.loading = false;

        this.bindListeners({
            updateLoading: actions.UPDATE_LOADING,
            updateSelected: actions.UPDATE_SELECTED,

            fetchProfile: actions.FETCH_SETTINGS,
            onSubmit: actions.ON_SUBMIT,
            generateKeys: actions.GENERATE_KEYS,

            updateSettings: actions.UPDATE_SETTINGS,
            errorupdateSettings: actions.ERRORUPDATE_SETTINGS,
        });

        this.registerAsync(source);
        
    }

    fetchProfile () {
        this.getInstance().fetchSettings();
    }

    onSubmit(childstate) {
        this.getInstance().onSubmit(childstate);
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




}


export default alt.createStore(SettingsStore, 'SettingsStore');