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

    submitProfile() {
        this.updateLoading(true);
        return true;
    }

    submitPassword() {
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

    updateSelected(name) {
        return name;
    }

    updateOldpassword(oldPassword) {
        return oldPassword;
    }

    updateNewpassword(newPassword) {
        return newPassword;
    }

    updateProfile(name, value) {
        return [name, value];
    }
        

}

export default alt.createActions(SettingsActions);