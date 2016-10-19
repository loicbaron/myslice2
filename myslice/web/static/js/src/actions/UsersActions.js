import alt from '../alt';

class UsersActions {

    fetchUsers(filter = {}) {
        return filter;
    }
    fetchProfile() {
        return true;
    }
    updateProfile(profile) {
        return profile;
    }
    setCurrentUser(user) {
        return user;
    }
    updateCurrentUser(user) {
        return user;
    }
    fetchFromUserAuthority(filter = {}) {
        return filter;
    }
    fetchFromAuthority() {
        return true;
    }
    updateAuthority(authority) {
        return authority;
    }
    updateUserElement(user) {
        return user;
    }

    updateUsers(users) {
        return users;
    }

    updateExcludeUsers(users) {
        return users;
    }
    updateFilter(filter) {
        return filter;
    }
    updateFilteredUsers() {
        return true;
    }
    errorUsers(errorMessage) {
        return errorMessage
    }

    grantPiRights(authority) {
        return authority;
    }
    revokePiRights(authority) {
        return authority;
    }

}

export default alt.createActions(UsersActions);


