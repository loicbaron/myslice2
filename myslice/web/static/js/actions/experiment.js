/**
 * Experiment view actions
 *
 */

class ExperimentActions {

    fetchSlices() {
        return (dispatch) => {
            // we dispatch an event here so we can have "loading" state.
            dispatch();
            axios.get('http://localhost:8111/api/v1/slices', {
                params: {
                    ID: 12345
                }
            }).then(function (response) {
                console.log(response);
                this.updateSlices(response.data.slices)

            }.bind(this)).catch(function (response) {
                console.log(response);
                this.errorSlices('error');
            }.bind(this));

        }
    }

    updateSlices(slices) {
        return slices;
    }

    errorSlices(errorMessage) {
        return errorMessage
    }
}

window.experimentactions = alt.createActions(ExperimentActions);