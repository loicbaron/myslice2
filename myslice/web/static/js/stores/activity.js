/**
 * Activity Store
 */

class ActivityStore {

    constructor() {
        this.activity = []
        this.errorMessage = null;

        this.bindListeners({
            updateActivityElement: activityactions.updateActivityElement,
            updateActivity: activityactions.updateActivity,

        });


    }

    updateActivityElement(activity) {
        console.log("STORAGE UPD ACTIVITY:" + activity.id)
        // Check if we already have this activity in the state
        let index = this.activity.findIndex(function(activityElement) {
            if (activityElement.id === activity.id) {
                return true;
            }
            return false;
        });
        /*  If we do we update it, otherwise we add a new
            activity event to the state (at the top of the array) */
        if (index !== -1) {
            this.activity[index] = activity;
        } else {
            this.activity.unshift(activity);
        }

        this.errorMessage = null;
        // optionally return false to suppress the store change event
    }

    updateActivity(activity) {
        this.activity = activity;
    }

}


window.activitystore = alt.createStore(ActivityStore, 'ActivityStore');

