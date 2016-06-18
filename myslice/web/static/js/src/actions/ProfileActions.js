import alt from '../alt';

class ProfileActions {

    fetchProfile() {
        return true;
    }

    onSubmit() {
        this.updateLoading(true);
        return true;
    }

    updateLoading(loading) {
        return loading;
    }

    updateUser(response) {
        this.updateLoading(false);
        return response;
    }

    errorupdateUser(error) {
        return error;
    }
    
    updateLastname(lastname) {
        return lastname;
    }

    updateFirstname(firstname) {
        return firstname;
    }

    updateBio(bio) {
        return bio;
    }

    updateUrl(url) {
        return url;
    }

}

export default alt.createActions(ProfileActions);