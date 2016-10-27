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

    submitResetPassword() {
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

    updateHashing(hashing) {
        return hashing;
    }

    updateProfile(name, value) {
        return [name, value];
    }

    successUpdatePassword(response) {
        this.updateLoading(false);
        return response;
    }
    errorUpdatePassword(response) {
        this.updateLoading(false);
        return response;
    }

}

export default alt.createActions(SettingsActions);
