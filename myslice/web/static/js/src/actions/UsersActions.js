import alt from '../alt';

class UsersActions {

    fetchUsers(filter = {}) {
        return filter;
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

}

export default alt.createActions(UsersActions);


