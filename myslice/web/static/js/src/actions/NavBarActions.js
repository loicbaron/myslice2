import alt from '../alt';

class NavBarActions {

    constructor() {
        this.generateActions(
            'fetchSlices',
            'setCurrentSlice',
            'getCurrentSlice',
            'updateSlices',
            'updateSliceElement',
            'showMenu'
        );
    }

}

export default alt.createActions(NavBarActions);


