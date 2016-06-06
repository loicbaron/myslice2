/**
 * Project actions
 *
 * Manages Events and Requests
 *
 */

class ProjectRequestActions {

    setupProject() {
        // fetch project
        this.fetchProject();

        var socket = new SockJS('/api/v1/live');

        socket.onopen = function() {
            /*
                Open websocket connection and watch for new/changed events
             */
            socket.send(JSON.stringify({'watch': 'activity', 'object':'PROJECT'}));

            console.log("open")
        };

        socket.onmessage = function(e) {
            /*
                Act upon receiving a message
             */
            let data = JSON.parse(e.data);
            console.log("Websocket:");
            console.log(data);

            this.updateProjectElement(data.activity);

        }.bind(this);

        socket.onclose = function() {
            console.log('close');
        };

        return false;
    }

    fetchProject() {
        return (dispatch) => {
            // we dispatch an event here so we can have "loading" state.
            dispatch();
            axios.get('/api/v1/activity?object=PROJECT', {
            }).then(function (response) {
                this.updateProject(response.data.activity);
                console.log(response.data.activity);
            }.bind(this)).catch(function (response) {
                this.errorProject('error');
                console.log(response);
            }.bind(this));

        }
    }

    updateProjectElement(project) {
        return project;
    }

    updateProject(project) {
        return project;
    }

    errorProject(errorMessage) {
        return errorMessage
    }

}

window.projectrequestactions = alt.createActions(ProjectRequestActions);

// setup project
projectrequestactions.setupProject();
