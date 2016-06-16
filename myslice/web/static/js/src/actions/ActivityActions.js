import alt from '../alt';

class ActivityActions {

    fetchActivity() {
        return true;
    }

    updateActivity(activity) {
        return activity;
    }

    errorActivity(errorMessage) {
        return errorMessage
    }

}

export default alt.createActions(ActivityActions);