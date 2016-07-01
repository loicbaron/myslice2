import alt from '../alt';
import actions from '../actions/RequestsActions';
import source from '../sources/RequestsSource';

class RequestsStore {

    constructor() {
        this.requests = [];
        this.errorMessage = null;
        this.action = {}
        this.id = "";

        this.bindListeners({
            updateActivityElement: actions.UPDATE_ACTIVITY_ELEMENT,
            updateRequests: actions.UPDATE_REQUESTS,

            handleAction: actions.HANDLE_ACTION,
            fetchRequests: actions.FETCH_REQUESTS,
            watchActivity: actions.WATCH_ACTIVITY,
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

    watchActivity() {}

    updateRequests(requests) {
        if (requests.hasOwnProperty('data')) {
            this.requests = requests.data.result;
        } else {
            this.requests = requests;
        }
    }


    updateActivityElement(activityElement) {
        // Check if we already have this activity in the state
        let index = this.activity.findIndex(function(needle) {
            return (needle.id === activityElement.id);
        });
        /*  If we do we update it, otherwise we add a new
            activity event to the state (at the top of the array) */
        if (index !== -1) {
            this.activity[index] = activityElement;
        } else {
            this.activity.unshift(activityElement);
        }

        this.errorMessage = null;
        // optionally return false to suppress the store change event
    }

    handleAction(data) {
        this.data = data;
        this.getInstance().handleAction();
    }

}


export default alt.createStore(RequestsStore, 'RequestsStore');

