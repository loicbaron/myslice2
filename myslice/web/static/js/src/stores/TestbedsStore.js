import alt from '../alt';
import actions from '../actions/TestbedsActions';
import source from '../sources/TestbedsSource';

class TestbedsStore {

    constructor() {
        this.testbeds = [];
        this.errorMessage = null;

        this.bindListeners({
            updateTestbedElement: actions.UPDATE_TESTBED_ELEMENT,
            updateTestbeds: actions.UPDATE_TESTBEDS,
            errorTestbeds: actions.ERROR_TESTBEDS,

            fetchTestbeds: actions.FETCH_TESTBEDS,
        });

        this.registerAsync(source);

    }

    fetchTestbeds(filter) {
        this.testbeds = [];
        this.filter = {};

        if (filter.length > 0) {
            filter.map(function (f) {
                this.filter[f.name].push(f.value);
            }.bind(this));
        }

        this.getInstance().fetchTestbeds();

    }

    updateTestbeds(testbeds) {
        if (testbeds.hasOwnProperty('data')) {
            this.testbeds = testbeds.data.result;
        } else {
            this.testbeds = testbeds;
        }
    }

    errorTestbeds(errorTestbeds) {}

    updateTestbedElement(testbedElement) {
        let index = this.requests.findIndex(function(needle) {
            return (needle.id === testbedElement.id);
        });
        /*  If we do we update it, otherwise we add a new
            requests event to the state (at the top of the array) */

        if (index !== -1) {
            this.testbeds[index] = testbedElement;
        } else {
            this.testbeds.unshift(testbedElement);
        }

        this.errorMessage = null;
        // optionally return false to suppress the store change event
    }

}


export default alt.createStore(TestbedsStore, 'TestbedsStore');

