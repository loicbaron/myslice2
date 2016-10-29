import alt from '../../alt';

class SelectResourceDialog {

    constructor() {
        this.generateActions(
            'updateTestbed',
            'fetchResources',
            'updateResources',
            'errorResources',
            'updateStartDate',
            'selectResource',
            'updateFilter'
        );
    }

}

export default alt.createActions(SelectResourceDialog);


