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
            'updateTime'
        );
    }

}

export default alt.createActions(SelectResourceDialog);


