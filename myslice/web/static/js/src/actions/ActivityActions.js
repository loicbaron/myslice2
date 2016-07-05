import alt from '../alt';
import SockJS from 'sockjs-client';

class ActivityActions {

    fetchActivity(filter = {}) {
        return filter;
    }

    watchActivity() {
        var socket = new SockJS('/api/v1/live');

        socket.onopen = function() {
            socket.send(JSON.stringify({'auth': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZG1pbiI6dHJ1ZSwicGlfYXV0aCI6WyJ1cm46cHVibGljaWQ6SUROK29uZWxhYithdXRob3JpdHkrc2EiLCJ1cm46cHVibGljaWQ6SUROK29uZWxhYjp1cG1jOmllZWUrYXV0aG9yaXR5K3NhIl0sImlkIjoidXJuOnB1YmxpY2lkOklETitvbmVsYWI6dXBtYyt1c2VyK2pvc2h6aG91MTYifQ.WQ_qCsVoXvfaP4G8m8WFCmujkMQrQ8vAypUlZNif2Dk'}))
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


}

export default alt.createActions(ActivityActions);