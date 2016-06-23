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

    submitProfile(childstate) {
        this.updateLoading(true);
        return childstate;
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

    repeatPassword(oldPassword) {
        return oldPassword;
    }

    resetPassword(newPassword) {
        return newPassword;
    }
        

}

export default alt.createActions(SettingsActions);