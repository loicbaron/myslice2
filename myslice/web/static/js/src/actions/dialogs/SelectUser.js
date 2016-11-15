import alt from '../../alt';

class SelectUserDialog {

    constructor() {
        this.generateActions(
            'fetchUsers',
            'updateUsers',
            'selectUser',
            'filterAuthority',

            'showSelected',
            'showAll',

            'updateFilter',
            'updateFilteredUsers',
            'updateUserElement',
            'fetchFromUserAuthority',
            'fetchFromAuthority',
            'updateAuthority',
            'errorUsers'
        );
    }

}

export default alt.createActions(SelectUserDialog);