import alt from '../alt';
import actions from '../actions/SliceViewActions';
import source from '../sources/SlicesSource';

class SlicesStore {

    constructor() {
        this.slices = [];

        this.filter = [];

        this.dialog = null;

        this.errorMessage = null;

        this.bindListeners({
            updateSliceElement: actions.UPDATE_SLICE_ELEMENT,
            updateSlices: actions.UPDATE_SLICES,
            fetchSlices: actions.FETCH_SLICES,
            errorSlices: actions.ERROR_SLICES,
        });

        this.registerAsync(source);
        
    }


    fetchSlices(filter) {

        this.filter = filter;

        if (!this.getInstance().isLoading()) {
            this.getInstance().fetch();
        }

    }

    updateSliceElement(slice) {
        let index = this.slices.findIndex(function(sliceElement) {
            return (sliceElement.id === slice.id);
        });

        if (index !== -1) {
            this.slices[index] = slice;
        } else {
            this.slices.unshift(slice);
        }

        this.errorMessage = null;
    }

    updateSlices(slices) {
        if (slices.hasOwnProperty('data')) {
            this.slices = slices.data.result;
        } else {
            this.slices = slices;
        }

        // check URL
        var u = window.location.href.toString().split(window.location.host)[1].split('/');
        var hrn = u.pop();
        var ctl = u.pop();

        if (ctl === 'slices') {
            this.setCurrentSlice(hrn);
        } else {
            this.setCurrentSlice();
        }

    }

    errorSlices(errorMessage) {
        console.log(errorMessage);
    }

}


export default alt.createStore(SlicesStore, 'SlicesStore');

