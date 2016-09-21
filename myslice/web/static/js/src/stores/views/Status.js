import alt from '../../alt';
import actions from '../../actions/views/Status';
import source from '../../sources/StatusViewSource';

class StatusViewStore {

    constructor() {

        this.testbeds = [];
        this.currentTestbed = null;

        this.resources = [];

        this.bindListeners({
            updateTestbedElement: actions.UPDATE_TESTBED_ELEMENT,
            updateTestbeds: actions.UPDATE_TESTBEDS,
            updateResourceElement: actions.UPDATE_RESOURCE_ELEMENT,
            updateResources: actions.UPDATE_RESOURCES,
            getTestbeds: actions.GET_TESTBEDS,
            setCurrentTestbed: actions.SET_CURRENT_TESTBED,
        });

        this.registerAsync(source);

    }

    getTestbeds() {

        if (!this.getInstance().isLoading()) {
            this.getInstance().testbeds();
        }

    }

    setCurrentTestbed(testbed) {
        this.currentTestbed = testbed;

        if (!this.getInstance().isLoading()) {
            this.getInstance().resources();
        }
    }

    updateTestbedElement(testbed) {
        let index = this.testbeds.findIndex(function(testbedElement) {
            return (testbedElement.id === testbed.id);
        });

        if (index !== -1) {
            this.testbeds[index] = testbed;
        } else {
            this.testbeds.unshift(testbed);
        }

        this.errorMessage = null;
    }

    updateTestbeds(testbeds) {
        if (testbeds.hasOwnProperty('data')) {
            this.testbeds = testbeds.data.result;
        } else {
            this.testbeds = testbeds;
        }
    }

    updateResourceElement(resource) {
        let index = this.resources.findIndex(function(resourceElement) {
            return (resourceElement.id === resource.id);
        });

        if (index !== -1) {
            this.resources[index] = resource;
        } else {
            this.resources.unshift(resource);
        }

        this.errorMessage = null;
    }

    updateResources(resources) {
        if (resources.hasOwnProperty('data')) {
            this.resources = resources.data.result;
        } else {
            this.resources = resources;
        }
    }


}


export default alt.createStore(StatusViewStore, 'StatusViewStore');

