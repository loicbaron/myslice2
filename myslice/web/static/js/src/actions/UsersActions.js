import alt from '../alt';

class UsersActions {

    fetchUsers(options) {
        return options;
    }

    updateUserElement(user) {
        return user;
    }

    updateUsers(user) {
        return user;
    }

    errorUsers(errorMessage) {
        return errorMessage
    }

}

export default alt.createActions(UsersActions);


