import alt from '../alt';

class SlicesActions {

    fetchSlices(options) {
        return options;
    }

    updateSliceElement(slice) {
        return slice;
    }

    updateSlices(slices) {
        return slices;
    }

    selectSlice(slice) {
        return slice;
    }

    errorSlices(errorMessage) {
        return errorMessage
    }

}

export default alt.createActions(SlicesActions);


