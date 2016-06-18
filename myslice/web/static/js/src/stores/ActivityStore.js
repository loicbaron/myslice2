import alt from '../alt';
import actions from '../actions/ActivityActions';
import source from '../sources/ActivitySource';

class ActivityStore {

    constructor() {
        this.activity = [];
        this.errorMessage = null;

        this.bindListeners({
            updateActivity: actions.UPDATE_ACTIVITY,
            updateActivityElement: actions.UPDATE_ACTIVITY_ELEMENT,
            fetchActivity: actions.FETCH_ACTIVITY,
            watchActivity: actions.WATCH_ACTIVITY,
        });

        this.registerAsync(source);

    }

    fetchActivity() {

        this.activity = [];

        if (!this.getInstance().isLoading()) {
            this.getInstance().fetch();
        }

    }

    watchActivity() {}

    updateActivity(activity) {
        if (activity.hasOwnProperty('data')) {
            this.activity = activity.data.result;
        } else {
            this.activity = activity;
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

}


export default alt.createStore(ActivityStore, 'ActivityStore');

