import alt from '../alt';
import actions from '../../actions/dialogs/SelectResource';
import source from '../../sources/resource/DialogSelect';

class ResourceDialogSelect {

    constructor() {
        // the id of the testbed
        this.testbed = null;
        // the list of resources
        this.resources = [];
        // the list of selected resources
        this.selected = [];

        this.errorMessage = null;

        this.bindListeners({
            fetchResources: actions.FETCH_RESOURCES,
            updateResources: actions.UPDATE_SLICE,
            errorResources: actions.ERROR_RESOURCES,

            selectResource: actions.ERROR_RESOURCE,

        });

        this.registerAsync(source);

    }


    fetchResources(testbed) {

        this.testbed = testbed;

        if (!this.getInstance().isLoading()) {
            this.getInstance().fetchResources();
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


export default alt.createStore(ResourceDialogSelect, 'ResourceDialogSelect');

