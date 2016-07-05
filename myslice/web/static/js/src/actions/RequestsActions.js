import alt from '../alt';
import SockJS from 'sockjs-client';

class RequestsActions {

    fetchRequests(filter = {}){
        return filter;
    }

    watchRequest() {
        var socket = new SockJS('/api/v1/live');
        let token = sessionStorage.getItem('token')

        socket.onopen = function() {
            socket.send(JSON.stringify({'auth': token}))
            socket.send(JSON.stringify({'watch': 'requests'}));
            console.log("open")
        };

        socket.onmessage = function(e) {
            let data = JSON.parse(e.data);
            this.updateRequestElement(data['request']);
        }.bind(this);

        socket.onclose = function() {
            console.log('close');
        };
        return true;
    }

    updateRequests(requests) {
        return requests;
    }

    updateRequestElement(requestElement) {
        return requestElement;
    }

    errorRequests(errorMessage) {
        return errorMessage;
    }

    executeAction(data) {
        return data;
    }

    executeSuccess(data) {
        return data;
    }

    executeError(errorMessage) {
        return errorMessage;
    }

}

export default alt.createActions(RequestsActions);