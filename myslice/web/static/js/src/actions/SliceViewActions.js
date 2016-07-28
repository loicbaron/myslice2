import alt from '../alt';

class SlicesActions {

    constructor() {
        this.generateActions(
            'fetchSlices',
            'updateSlices',
            'updateSliceElement',
            'errorSlices'
        );
    }

}

export default alt.createActions(SlicesActions);


