import alt from '../alt';

class UsersActions {

    fetchUsers(filter = {}) {
        return filter;
    }

    fetchFromAuthority(filter = {}) {
        return filter;
    }

    updateUserElement(user) {
        return user;
    }

    updateUsers(user) {
        return user;
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


