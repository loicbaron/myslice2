import alt from '../alt';

class SettingsActions {

    fetchSettings() {
        return true;
    }

    updateSettings(response) {
        this.updateLoading(false);
        return response;
    }

    errorupdateSettings(response) {
        this.updateLoading(false);
        return response;
    }

    onSubmit() {
        console.log('set loading ture')
        this.updateLoading(true);
        return true;
    }

    generateKeys(){
        this.updateLoading(true);
        return true;
    }

    updateLoading(loading) {
        return loading;
    }
        

}

export default alt.createActions(SettingsActions);