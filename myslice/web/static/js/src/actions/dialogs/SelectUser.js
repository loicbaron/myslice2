import alt from '../../alt';

class SelectUserDialog {

    constructor() {
        this.generateActions(
            'fetchUsers',
            'updateUsers',
            'errorUsers',

            'selectUser',
            'clearSelection',
            'showSelected',
            'showAll',

            'filterAuthority',
            'filterUser'

        );
    }

}

export default alt.createActions(SelectUserDialog);