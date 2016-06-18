import alt from '../alt';
import SockJS from 'sockjs-client';

class ActivityActions {

    fetchActivity() {
        return true;
    }

    watchActivity() {
        var socket = new SockJS('/api/v1/live');

        socket.onopen = function() {
            socket.send(JSON.stringify({'watch': 'activity'}));
            console.log("open")
        };

        socket.onmessage = function(e) {
            let data = JSON.parse(e.data);
            this.updateActivityElement(data);
        }.bind(this);

        socket.onclose = function() {
            console.log('close');
        };
        return true;
    }

    updateActivity(activity) {
        return activity;
    }

    updateActivityElement(activityElement) {
        return activityElement;
    }

    errorActivity(errorMessage) {
        return errorMessage
    }

}

export default alt.createActions(ActivityActions);