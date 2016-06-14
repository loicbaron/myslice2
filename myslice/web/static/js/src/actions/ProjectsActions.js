import alt from '../alt';

class ProjectsActions {

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

    fetchProjects() {
        return true;
    }

    updateProjectElement(project) {
        return project;
    }

    updateProjects(project) {
        return project;
    }

    selectProject(project) {
        return project;
    }

    errorProjects(errorMessage) {
        return errorMessage
    }

}

module.exports = alt.createActions(ProjectsActions);


