import alt from '../alt';
import actions from '../actions/views/Slice';
import source from '../sources/SliceView';

/*
    This store is used in the SliceView
 */
class SliceView {

    constructor() {
        // the hrn of the current slice
        this.hrn = null;
        // the current slice
        this.slice = [];
        // the list of testbeds
        this.testbeds = [];

        this.dialog = null;

        this.errorMessage = null;

        this.bindListeners({
            updateSlice: actions.UPDATE_SLICE,
            fetchSlice: actions.FETCH_SLICE,
            errorSlice: actions.ERROR_SLICE,

            updateTestbeds: actions.UPDATE_TESTBEDS,
            fetchTestbeds: actions.FETCH_TESTBEDS,
            errorTestbeds: actions.ERROR_TESTBEDS,
        });

        this.registerAsync(source);
        
    }


    fetchSlice(hrn) {

        this.hrn = hrn;

        if (!this.getInstance().isLoading()) {
            this.getInstance().fetchSlice();
        }

    }

    updateSlice(slice) {
        if (slice.hasOwnProperty('data')) {
            this.slice = slice.data.result[0];
        } else {
            this.slice = slice;
        }

    }

    errorSlice(errorMessage) {
        console.log(errorMessage);
    }

    fetchTestbeds() {
        this.getInstance().fetchTestbeds();
    }

    updateTestbeds(testbeds) {
        if (testbeds.hasOwnProperty('data')) {
            this.testbeds = testbeds.data.result;
        } else {
            this.testbeds = testbeds;
        }

    }

    errorTestbeds(errorMessage) {
        console.log(errorMessage);
    }

    showDialog(dialog) {
        this.dialog = dialog;
    }

}


export default alt.createStore(SliceView, 'SliceView');

