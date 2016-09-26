import alt from '../alt';

class TestbedsActions {

    constructor() {
        this.generateActions(
            'fetchTestbeds',
            'updateTestbeds',
            'updateTestbedElement',
            'errorTestbed',
        );
    }

}

export default alt.createActions(TestbedsActions);


