import alt from '../alt';

class SliceView {

    constructor() {
        this.generateActions(
            'fetchSlice',
            'updateSlice',
            'errorSlice',

            'fetchTestbeds',
            'updateTestbeds',
            'errorTestbeds',

            'showDialog'
        );
    }

}

export default alt.createActions(SliceView);


