import alt from '../../alt';

class SelectResourceDialog {

    constructor() {
        this.generateActions(
            'updateTestbed',
            'fetchResources',
            'updateResources',
            'errorResources',

            'selectResource'
        );
    }

}

export default alt.createActions(SelectResourceDialog);


