import alt from '../alt';

class ResourceDialogSelect {

    constructor() {
        this.generateActions(
            'fetchResources',
            'updateResources',
            'errorResources',

            'selectResource'
        );
    }

}

export default alt.createActions(ResourceDialogSelect);


