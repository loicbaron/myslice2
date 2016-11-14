import alt from '../../alt';
import actions from '../../actions/dialogs/SelectUser';
import source from '../../sources/dialogs/SelectUser';

class SelectUserDialog {

    constructor() {

        // User List as retrieved from the API
        this.users = [];

        // Filtered users
        this.filtered = [];

        // Selected users
        this.selected = [];

        this.authority = {
            id: null
        };

        this.filter = {};

        this.errorMessage = null;

        this.bindListeners({
            updateUserElement: actions.UPDATE_USER_ELEMENT,
            updateUsers: actions.UPDATE_USERS,

            updateFilter: actions.UPDATE_FILTER,
            updateFilteredUsers: actions.UPDATE_FILTERED_USERS,

            fetchUsers: actions.FETCH_USERS,

            fetchFromUserAuthority: actions.FETCH_FROM_USER_AUTHORITY,
            fetchFromAuthority: actions.FETCH_FROM_AUTHORITY,
            updateAuthority: actions.UPDATE_AUTHORITY,
            errorUsers: actions.ERROR_USERS,

        });

        this.registerAsync(source);
    }

    fetchUsers(filter) {
        this.filter = filter;

        this.users = [];

        if (!this.getInstance().isLoading()) {
            this.getInstance().fetchUsers();
        }
    }

    fetchFromUserAuthority(filter) {
        this.filter = filter;

        if (!this.getInstance().isLoading()) {
            this.getInstance().fetchFromUserAuthority();
        }
    }

    fetchFromAuthority() {
        if (!this.getInstance().isLoading()) {
            this.getInstance().fetchFromAuthority();
        }
    }

    updateAuthority(authority) {
        this.authority = authority;
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
        /*
        var exUsers = this.excludeUsers;
        var excludeU = function(el){
            for (var i=0; i<exUsers.length; i++) {
                if(exUsers[i] == el.id){
                    return false;
                    break;
                }
            }
            return true;
        };

        if (Object.keys(this.filter).length>0) {
            if (users.hasOwnProperty('data')) {
                this.filteredUsers = users.data.result;
            } else {
                this.filteredUsers = users;
            }
            if(exUsers.length>0){
                this.filteredUsers = this.filteredUsers.filter(function(el){
                    return excludeU(el);
                });
            }

        } else {
        */
            if (users.hasOwnProperty('data')) {
                this.users = users.data.result;
            } else {
                this.users = users;
            }
            /*
            if(exUsers.length>0){
                this.users = this.users.filter(function(el){
                    return excludeU(el);
                });
            }

        }
        */
    }

    updateFilter(filter) {
        this.filter = filter;
        if(Object.keys(filter).length==0){
            this.filteredUsers = [];
        }
    }

    updateFilteredUsers() {
        var f = this.filter;
        var checkU = function(el){
            for (var k in f) {
                if(el[k].indexOf(f[k]) > -1){
                    return true;
                    break;
                }
            }
            return false;
        };
        this.filteredUsers = this.users.filter(function(el){
            return checkU(el);
        });
    }

    errorUsers(errorMessage) {
        console.log(errorMessage);
    }

}


export default alt.createStore(SelectUserDialog, 'SelectUserDialog');

