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

        // Current Authority ID
        this.authority = null;

        // if true shows selected
        this.show_selected = false;

        this.errorMessage = null;

        this.bindListeners({
            fetchUsers: actions.FETCH_USERS,
            updateUsers: actions.UPDATE_USERS,
            selectUser: actions.SELECT_USER,
            filterAuthority: actions.FILTER_AUTHORITY,

            showSelected: actions.SHOW_SELECTED,
            showAll: actions.SHOW_ALL,


            updateUserElement: actions.UPDATE_USER_ELEMENT,




            updateFilter: actions.UPDATE_FILTER,
            updateFilteredUsers: actions.UPDATE_FILTERED_USERS,



            fetchFromUserAuthority: actions.FETCH_FROM_USER_AUTHORITY,
            fetchFromAuthority: actions.FETCH_FROM_AUTHORITY,
            updateAuthority: actions.UPDATE_AUTHORITY,
            errorUsers: actions.ERROR_USERS,

        });

        this.registerAsync(source);
    }

    fetchUsers() {

        this.users = [];

        if (!this.getInstance().isLoading()) {
            this.getInstance().fetchUsers();
        }
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

    filterAuthority(authority) {
        this.authority = authority;
        this.fetchUsers();
    }

    selectUser(user) {
        let userId = this.selected.some(function(el) {
            return el.id === user.id;
        });

        if (!userId) {
            this.selected.push(user);
        } else {
            this.selected = this.selected.filter(function(el) {
                return el.id !== user.id;
            });
        }

        if (this.selected.length == 0) {
            this.showAll();
        }
    }

    showSelected() {
        this.show_selected = true;
    }

    showAll() {
        this.show_selected = false;
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

