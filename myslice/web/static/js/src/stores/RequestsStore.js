import alt from '../alt';
import actions from '../actions/RequestsActions';
import source from '../sources/RequestsSource';

class RequestsStore {

    constructor() {
        this.requests = [];
        this.errorMessage = null;

        this.bindListeners({
            updateRequestElement: actions.UPDATE_REQUEST_ELEMENT,
            updateRequests: actions.UPDATE_REQUESTS,
            errorRequests: actions.ERROR_REQUESTS,

            executeSuccess: actions.EXECUTE_SUCCESS,
            executeError: actions.EXECUTE_ERROR,

            executeAction: actions.EXECUTE_ACTION,
            fetchRequests: actions.FETCH_REQUESTS,
        });

        this.registerAsync(source);

    }

    fetchRequests(filter) {
        this.requests = [];
        this.filter = {
            'action': [],
            'status': [],
            'object': []
        };

        if (filter.length > 0) {
            filter.map(function (f) {
                this.filter[f.name].push(f.value);
            }.bind(this));
        }

        this.getInstance().fetchRequests();

    }

    updateRequests(requests) {
        if (requests.hasOwnProperty('data')) {
            this.requests = requests.data.result;
        } else {
            this.requests = requests;
        }
    }

    errorRequests(errorRequests) {}

    updateRequestElement(requestElement) {
        // Check if we already have this requests in the state

        let index = this.requests.findIndex(function(needle) {
            return (needle.id === requestElement.id);
        });
        /*  If we do we update it, otherwise we add a new
            requests event to the state (at the top of the array) */
        
        if (index !== -1) {
            this.requests[index] = requestElement;
        } else {
            this.requests.unshift(requestElement);
        }

        this.errorMessage = null;
        // optionally return false to suppress the store change event
    }

    executeAction(data) {
        
        // find the request we are executing and remove it.
        let index = this.requests.findIndex(function(needle) {
            return (needle.id === data.id);
        });
        this.requests.splice(index, 1);
        
        this.data = data;
        this.getInstance().executeAction();
    }

    executeSuccess(data) {}

    executeError(errorMessage) {}


}


export default alt.createStore(RequestsStore, 'RequestsStore');

