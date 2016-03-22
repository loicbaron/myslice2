/**
 * Experiment Store
 */

class ExperimentStore {

    constructor() {
        this.slices = []

        this.errorMessage = null;

        this.bindListeners({
            updateSlices: experimentactions.UPDATE_SLICES,
            fetchSlices: experimentactions.FETCH_SLICES,
            errorSlices: experimentactions.ERROR_SLICES
        });
    }

    fetchSlices() {
        // reset the array while we're fetching new slices so React can
        // be smart and render a spinner for us since the data is empty.
        this.slices = [];
    }

    errorSlices(errorMessage) {
        this.errorMessage = errorMessage;
    }

    updateSlices(slices) {

        this.slices = slices;
        this.errorMessage = null;
        // optionally return false to suppress the store change event
    }
}


window.experimentstore = alt.createStore(ExperimentStore, 'ExperimentStore');

