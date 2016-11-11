import alt from '../../alt';

class SelectUserDialog {

    constructor() {
        this.generateActions(
            'fetchUsers',
            'fetchResources',
            'updateResources',
            'errorResources',
            'updateStartDate',
            'updateType',
            'selectResource',
            'updateFilter',
            'updateTime',
            'submitReservation',
            'successReservation',
            'errorreservation'
        );
    }

}

export default alt.createActions(SelectUserDialog);