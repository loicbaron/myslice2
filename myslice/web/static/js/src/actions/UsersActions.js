import alt from '../alt';

class UsersActions {

    setupUser() {
        // fetch user
        this.fetchUser();

        var socket = new SockJS('/api/v1/live');

        socket.onopen = function() {
            /*
                Open websocket connection and watch for new/changed events
             */
            socket.send(JSON.stringify({'watch': 'users'}));

            console.log("open users")
        };

        socket.onmessage = function(e) {
            /*
                Act upon receiving a message
             */
            let data = JSON.parse(e.data);

            console.log("users");
            console.log(data)

            this.updateUserElement(data.users);

        }.bind(this);

        socket.onclose = function() {
            console.log('close users');
        };

        return false;
    }

    fetchUsers(filter={}) {
        return filter;
    }

    updateUserElement(user) {
        return user;
    }

    updateUsers(user) {
        return user;
    }

    selectUser(user) {
        return user;
    }

    errorUsers(errorMessage) {
        return errorMessage
    }

}

export default alt.createActions(UsersActions);


