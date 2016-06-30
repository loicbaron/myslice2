import alt from '../alt';

class NavActions {

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

}

export default alt.createActions(NavActions);


