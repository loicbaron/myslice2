import alt from '../alt';
import actions from '../actions/UsersActions';
import source from '../sources/UsersSource';

class UsersStore {

    constructor() {
        this.users = [];
        this.options = {
            filter: [],
            belongTo: {
                type: null,
                object: null
            }
        };
        this.errorMessage = null;

        this.bindListeners({
            updateUserElement: actions.UPDATE_USER_ELEMENT,
            updateUsers: actions.UPDATE_USERS,
            fetchUsers: actions.FETCH_USERS,
            errorUsers: actions.ERROR_USERS
            
        });

        this.registerAsync(source);
    }

    fetchUsers(options) {

        this.options = options;

        if (!this.getInstance().isLoading()) {
            this.getInstance().fetch();
        }

    }

    updateUserElement(user) {
        let index = this.users.findIndex(function(userElement) {
            return (userElement.id === user.id);
        });
        if (index !== -1) {
            this.users[index] = user;
        } else {
            this.users.unshift(user);
        }

        this.errorMessage = null;
    }

    updateUsers(users) {
        if (users.hasOwnProperty('data')) {
            this.users = users.data.result;
        } else {
            this.users = users;
        }
    }

    errorUsers(errorMessage) {
        console.log(errorMessage);
    } 

}


export default alt.createStore(UsersStore, 'UsersStore');

