import alt from '../../alt';

class SelectResourceDialog {

    constructor() {
        this.generateActions(
            'fetchResources',
            'updateResources',
            'errorResources',

            'selectResource',
            'clearSelection',
            'showSelected',
            'showAll',
            'filterResources',


            'updateTestbed',


            'updateStartDate',
            'updateType',
            'updateFilter',
            'updateTime',
            'submitReservation',
            'successReservation',
            'errorReservation'
        );
    }

}

export default alt.createActions(SelectResourceDialog);


