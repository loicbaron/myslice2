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
            errorUsers: actions.ERROR_USERS,

            selectUser: actions.SELECT_USER,
            clearSelection: actions.CLEAR_SELECTION,
            showSelected: actions.SHOW_SELECTED,
            showAll: actions.SHOW_ALL,

            filterAuthority: actions.FILTER_AUTHORITY,
            filterUser: actions.FILTER_USER,

        });

        this.registerAsync(source);
    }

    fetchUsers() {

        this.users = [];
        this.filtered = [];

        if (!this.getInstance().isLoading()) {
            this.getInstance().fetchUsers();
        }
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

    clearSelection() {
        this.selected = [];
        this.showAll();
    }

    showSelected() {
        this.show_selected = true;
    }

    showAll() {
        this.show_selected = false;
    }

    filterAuthority(authority) {
        this.authority = authority;
        this.fetchUsers();
    }

    filterUser(value) {
        if (value) {
            this.filtered = this.users.filter(function(el) {
                return el.email.indexOf(value) > -1 ||
                        el.shortname.indexOf(value) > -1 ;
                        //el.first_name.indexOf(value) > -1 ||
                        //el.last_name.indexOf(value) > -1;
            });
        } else {
            this.filtered = [];
        }
    }
}


export default alt.createStore(SelectUserDialog, 'SelectUserDialog');

