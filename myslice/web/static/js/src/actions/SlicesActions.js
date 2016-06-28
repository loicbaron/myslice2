import alt from '../alt';

class SlicesActions {

    constructor() {
        this.generateActions(
            'fetchSlices',
            'setCurrentSlice',
            'getCurrentSlice',
            'updateSlices',
            'updateSliceElement',
            'errorSlices',
            'showMenu'
        );
    }

    getCurrentSlice() {
        return;
    }

}

export default alt.createActions(SlicesActions);


