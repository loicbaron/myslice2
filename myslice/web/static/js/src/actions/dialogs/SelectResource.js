import alt from '../../alt';

class SelectResourceDialog {

    constructor() {
        this.generateActions(
            'updateTestbed',
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
            'errorReservation'
        );
    }

}

export default alt.createActions(SelectResourceDialog);


