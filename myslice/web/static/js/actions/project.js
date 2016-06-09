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

            console.log("open projects")
        };

        socket.onmessage = function(e) {
            /*
                Act upon receiving a message
             */
            let data = JSON.parse(e.data);

            console.log("projects");
            console.log(data)

            this.updateProjectElement(data.projects);

        }.bind(this);

        socket.onclose = function() {
            console.log('close projects');
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
        }
    }

    updateProjectElement(project) {
        return project;
    }

    updateProject(project) {
        return project;
    }
    selectProject(project) {
        return project;
    }

    errorProject(errorMessage) {
        return errorMessage
    }

}

window.projectactions = alt.createActions(ProjectActions);

// setup project
projectactions.setupProject();
