import alt from '../alt';
import SockJS from 'sockjs-client';

class RequestsActions {

    fetchRequests(filter = {}){
        return filter;
    }

    watchRequest() {
        var socket = new SockJS('/api/v1/live');

        socket.onopen = function() {
            socket.send(JSON.stringify({'auth': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZG1pbiI6dHJ1ZSwicGlfYXV0aCI6WyJ1cm46cHVibGljaWQ6SUROK29uZWxhYithdXRob3JpdHkrc2EiLCJ1cm46cHVibGljaWQ6SUROK29uZWxhYjp1cG1jOmllZWUrYXV0aG9yaXR5K3NhIl0sImlkIjoidXJuOnB1YmxpY2lkOklETitvbmVsYWI6dXBtYyt1c2VyK2pvc2h6aG91MTYifQ.WQ_qCsVoXvfaP4G8m8WFCmujkMQrQ8vAypUlZNif2Dk'}))
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