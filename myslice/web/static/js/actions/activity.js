/**
 * Activity actions
 *
 * Manages Events and Requests
 *
 */

class ActivityActions {

    setupActivity() {
        // fetch activity
        this.fetchActivity();

        var socket = new SockJS('/api/v1/live');

        socket.onopen = function() {
            /*
                Open websocket connection and watch for new/changed events
             */
            socket.send(JSON.stringify({'watch': 'activity'}));

            console.log("open")
        };

        socket.onmessage = function(e) {
            /*
                Act upon receiving a message
             */
            let data = JSON.parse(e.data);

            console.log(data)

            this.updateActivityElement(data.activity);

        }.bind(this);

        socket.onclose = function() {
            console.log('close');
        };

        return false;
    }

    fetchActivity() {
        return (dispatch) => {
            // we dispatch an event here so we can have "loading" state.
            dispatch();
            axios.get('/api/v1/activity', {
            }).then(function (response) {
                this.updateActivity(response.data.activity);
                console.log(response.data.activity);

            }.bind(this)).catch(function (response) {
                this.errorActivity('error');
                console.log(response);
            }.bind(this));

        }
    }

    updateActivityElement(activity) {
        return activity;
    }

    updateActivity(activity) {
        return activity;
    }

    errorActivity(errorMessage) {
        return errorMessage
    }

}

window.activityactions = alt.createActions(ActivityActions);

// setup activity
activityactions.setupActivity();
