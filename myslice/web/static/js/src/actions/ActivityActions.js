import alt from '../alt';
import SockJS from 'sockjs-client';

class ActivityActions {

    getUserToken() {
        return true;
    }

    fetchActivity(filter = {}) {
        return filter;
    }

    watchActivity() {
        var socket = new SockJS('/api/v1/live');
        let token = sessionStorage.getItem('token');

        socket.onopen = function() {
            socket.send(JSON.stringify({'auth' : token}))
            socket.send(JSON.stringify({'watch': 'activity'}));
            console.log("open")
        };

        socket.onmessage = function(e) {
            let data = JSON.parse(e.data);
            this.updateActivityElement(data['activity']);
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
        return errorMessage;
    }

    setUserToken(data) {
        return data;
    }

    filterEvent(value) {
        return value;
    }
}

export default alt.createActions(ActivityActions);
