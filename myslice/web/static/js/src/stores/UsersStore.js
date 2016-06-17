import alt from '../alt';
import actions from '../actions/UsersActions';
import source from '../sources/UsersSource';

class UsersStore {

    constructor() {
        this.users = [];
        this.errorMessage = null;

        this.bindListeners({
            updateUserElement: actions.UPDATE_USER_ELEMENT,

            updateUsers: actions.UPDATE_USERS,
            fetchUsers: actions.FETCH_USERS,
            errorUsers: actions.ERROR_USERS
            
        });

        this.registerAsync(source);
    }

    fetchUsers() {

        if (!this.getInstance().isLoading()) {
            this.getInstance().fetch();
        }

    }

    updateUserElement(user) {
        console.log("STORAGE UPD ACTIVITY:" + user.id)
        // Check if we already have this user in the state
        let index = this.users.findIndex(function(userElement) {
            if (userElement.id === user.id) {
                return true;
            }
            return false;
        });
        /*  If we do we update it, otherwise we add a new
            user event to the state (at the top of the array) */
        if (index !== -1) {
            this.users[index] = user;
        } else {
            this.users.unshift(user);
        }

        this.errorMessage = null;
        // optionally return false to suppress the store change event
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

