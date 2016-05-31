/**
 * Project actions
 *
 * Manages Events and Requests
 *
 */

class ProjectActions {

    setupProject() {
        // fetch project
        this.fetchProject();

        var socket = new SockJS('/api/v1/live');

        socket.onopen = function() {
            /*
                Open websocket connection and watch for new/changed events
             */
            socket.send(JSON.stringify({'watch': 'projects'}));
            socket.send(JSON.stringify({'watch': 'activity', 'object':'PROJECT'}));

            console.log("open")
        };

        socket.onmessage = function(e) {
            /*
                Act upon receiving a message
             */
            let data = JSON.parse(e.data);

            console.log(data)

            this.updateProjectElement(data.project);

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
            axios.get('/api/v1/projects', {
            }).then(function (response) {
                this.updateProject(response.data.result);
                console.log(response.data.result);
            }.bind(this)).catch(function (response) {
                this.errorProject('error');
                console.log(response);
            }.bind(this));

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

window.projectactions = alt.createActions(ProjectActions);

// setup project
projectactions.setupProject();
