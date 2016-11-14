import alt from '../../alt';

class SelectUserDialog {

    constructor() {
        this.generateActions(
            'updateUsers',
            'updateUserElement',

            'updateFilter',
            'updateFilteredUsers',

            'fetchUsers',

            'fetchFromUserAuthority',
            'fetchFromAuthority',
            'updateAuthority',
            'errorUsers'
        );
    }

}

export default alt.createActions(SelectUserDialog);