import alt from '../alt';
import axios from 'axios';
import UserProfileStore from '../stores/UserProfileStore';

class UserProfileActions {

    initUser() {
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

export default alt.createActions(UserProfileActions);