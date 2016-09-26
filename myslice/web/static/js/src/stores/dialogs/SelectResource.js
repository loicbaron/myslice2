import alt from '../../alt';
import actions from '../../actions/dialogs/SelectResource';
import source from '../../sources/dialogs/SelectResource';

class SelectResourceDialog {

    constructor() {
        // the testbed
        this.testbed = null;
        // the list of resources
        this.resources = [];
        // the list of selected resources
        this.selected = [];

        this.errorMessage = null;

        this.bindListeners({
            updateTestbed: actions.UPDATE_TESTBED,
            fetchResources: actions.FETCH_RESOURCES,
            updateResources: actions.UPDATE_RESOURCES,
            errorResources: actions.ERROR_RESOURCES,

            selectResource: actions.SELECT_RESOURCE,

        });

        this.registerAsync(source);

    }

    updateTestbed(testbed) {
        this.testbed = testbed;
    }

    fetchResources() {

        if (!this.getInstance().isLoading()) {
            this.getInstance().resources();
        }

    }

    updateResources(resources) {
        if (resources.hasOwnProperty('data')) {
            this.resources = resources.data.result;
        } else {
            this.resources = resources;
        }

    }

    errorResources(errorMessage) {
        console.log(errorMessage);
    }

    selectResource(resource) {
        this.selected = resource;
    }

}


export default alt.createStore(SelectResourceDialog, 'SelectResourceDialog');

