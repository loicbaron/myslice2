import alt from '../alt';
import actions from '../actions/ActivityActions';
import source from '../sources/ActivitySource';

class ActivityStore {

    constructor() {
        this.activity = [];
        this.errorMessage = null;

        this.bindListeners({
            updateActivity: actions.UPDATE_ACTIVITY,
            fetchActivity: actions.FETCH_ACTIVITY,
        });

        this.registerAsync(source);

    }

    fetchActivity() {

        this.activity = [];

        if (!this.getInstance().isLoading()) {
            this.getInstance().fetch();
        }

    }

    updateActivity(activity) {
        if (activity.hasOwnProperty('data')) {
            this.activity = activity.data.result;
        } else {
            this.activity = activity;
        }
    }

}


export default alt.createStore(ActivityStore, 'ActivityStore');

