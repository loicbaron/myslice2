/**
 * Activity actions
 *
 * Manages Events and Requests
 *
 */

class ActivityActions {

    setupActivity() {

        this.fetchEvents();

        var socket = new SockJS('http://localhost:8111/api/v1/live');

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
            console.log(e.data)
            this.updateEvent(data);

        }.bind(this);

        socket.onclose = function() {
            console.log('close');
        };

        return false;
    }

    fetchEvents() {
        return (dispatch) => {
            // we dispatch an event here so we can have "loading" state.
            dispatch();
            axios.get('/api/v1/events', {
                params: {
                    ID: 12345
                }
            }).then(function (response) {
                this.updateEvents(response.data.events);

            }.bind(this)).catch(function (response) {
                this.errorEvent('error');
            }.bind(this));

        }
    }

    updateEvent(event) {
        return event;
    }
    updateEvents(events) {
        return events;
    }

    errorEvent(errorMessage) {
        return errorMessage
    }

    fetchRequests() {
        return (dispatch) => {
            // we dispatch an event here so we can have "loading" state.
            dispatch();
            axios.get('/api/v1/requests', {
                params: {
                    ID: 12345
                }
            }).then(function (response) {
                this.updateRequests(response.data.requests)

            }.bind(this)).catch(function (response) {
                this.errorRequest('error');
            }.bind(this));

        }
    }

    updateRequest(request) {
        return request;
    }

    updateRequests(requests) {
        return requests;
    }

    errorRequest(errorMessage) {
        return errorMessage
    }




}

window.activityactions = alt.createActions(ActivityActions);