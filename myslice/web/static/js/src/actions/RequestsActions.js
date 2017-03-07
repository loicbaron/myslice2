import alt from '../alt';
import SockJS from 'sockjs-client';

class RequestsActions {

    fetchRequests(filter = {}){
        return filter;
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