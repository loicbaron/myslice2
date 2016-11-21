import alt from '../alt';

class NavBarActions {

    constructor() {
        this.generateActions(
            'fetchSlices',
            'fetchProjects',
            'setCurrentSlice',
            'getCurrentSlice',
            'updateSlices',
            'updateProjects',
            'updateSliceElement',
            'showMenu'
        );
    }

}

export default alt.createActions(NavBarActions);


