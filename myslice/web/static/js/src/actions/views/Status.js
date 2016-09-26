import alt from '../../alt';

class StatusViewActions {

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

export default alt.createActions(StatusViewActions);


