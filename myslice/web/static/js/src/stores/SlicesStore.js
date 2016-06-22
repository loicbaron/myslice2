import alt from '../alt';
import actions from '../actions/SlicesActions';
import source from '../sources/SlicesSource';

class SlicesStore {

    constructor() {
        this.slices = [];
        this.selected = null;
        this.options = {
            filter: [],
            belongTo: {
                type: null,
                object: null
            }
        };
        this.errorMessage = null;

        this.bindListeners({
            updateSliceElement: actions.UPDATE_SLICE_ELEMENT,
            updateSlices: actions.UPDATE_SLICES,
            fetchSlices: actions.FETCH_SLICES,
            errorSlices: actions.ERROR_SLICES

        });

        this.registerAsync(source);
    }

    fetchSlices(options) {

        this.options = options;

        if (!this.getInstance().isLoading()) {
            this.getInstance().fetch();
        }

    }

    updateSliceElement(slice) {
        let index = this.projects.findIndex(function(sliceElement) {
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
    }

    selectSlice(slice) {
        this.selected = slice;
    }

    errorSlices(errorMessage) {
        console.log(errorMessage);
    }

}


export default alt.createStore(SlicesStore, 'SlicesStore');

