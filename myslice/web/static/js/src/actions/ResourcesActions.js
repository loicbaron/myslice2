import alt from '../alt';

class ResourcesActions {

    constructor() {
        this.generateActions(
            'getTestbeds',
            'updateTestbeds',
            'updateTestbedElement',
            'updateResources',
            'updateResourceElement',
            'setCurrentTestbed',
            'errorTestbed',
            'errorResource'
        );
    }

}

export default alt.createActions(ResourcesActions);


