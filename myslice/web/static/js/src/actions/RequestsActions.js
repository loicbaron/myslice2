import alt from '../alt';
import SockJS from 'sockjs-client';

class RequestsActions {

    fetchRequests(filter = {}){
        return filter;
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

    updateRequests(requests) {
        return requests;
    }

    updateActivityElement(activityElement) {
        return activityElement;
    }

    errorRequests(errorMessage) {
        return errorMessage;
    }

    handleAction(data) {
        return data;
    }
}

export default alt.createActions(RequestsActions);