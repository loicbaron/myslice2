import alt from '../../alt';

class SliceView {

    constructor() {
        this.generateActions(
            'fetchSlice',
            'updateSlice',
            'errorSlice',

            'fetchTestbeds',
            'updateTestbeds',
            'errorTestbeds',

            'selectResourceDialog',
            'selectUserDialog',
            'closeDialog'
        );
    }

}

export default alt.createActions(SliceView);


