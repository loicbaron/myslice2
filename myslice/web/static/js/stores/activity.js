/**
 * Activity Store
 */

class ActivityStore {

    constructor() {
        this.events = []
        this.requests = []
        this.errorMessage = null;

        this.bindListeners({
            updateEvent: activityactions.updateEvent,
            updateEvents: activityactions.updateEvents,
            updateRequest: activityactions.updateRequest,
            updateRequests: activityactions.updateRequests,
        });


    }

    updateEvent(event) {
        console.log("STORAGE UPD EVENT:" + event.id)
        // Check if we already have this activity in the state
        let index = this.events.findIndex(function(eventElement) {
            if (eventElement.id === event.id) {
                return true;
            }
            return false;
        })
        /*  If we do we update it, otherwise we add a new
            activity event to the state (at the top of the array) */
        if (index !== -1) {
            this.events[index] = event;
        } else {
            this.events.unshift(event);
        }

        this.errorMessage = null;
        // optionally return false to suppress the store change event
    }
    updateEvents(events) {
        this.events = events;
    }

    updateRequest(request) {
        console.log("STORAGE UPD REQUEST:" + request.id)
        // Check if we already have this activity in the state
        let index = this.requests.findIndex(function(requestElement) {
            if (requestElement.id === request.id) {
                return true;
            }
            return false;
        })
        /*  If we do we update it, otherwise we add a new
            activity event to the state (at the top of the array) */
        if (index !== -1) {
            this.requests[index] = request;
        } else {
            this.requests.unshift(request);
        }

        this.errorMessage = null;
        // optionally return false to suppress the store change event
    }

    updateRequests(requests) {
        this.requests = requests;
    }

}


window.activitystore = alt.createStore(ActivityStore, 'ActivityStore');

