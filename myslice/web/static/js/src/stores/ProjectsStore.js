var alt = require('../alt');
var actions = require('../actions/ProjectsActions');
var source = require('../sources/ProjectsSource');

class ProjectsStore {

    constructor() {
        this.projects = [];
        this.errorMessage = null;
        this.selected = null;

        this.bindListeners({
            updateProjectElement: actions.updateProjectElement,
            updateProjects: actions.updateProjects,
            selectProject: actions.selectProject,
            fetchProjects: actions.fetchProjects,
        });

        this.registerAsync(source);
    }

    fetchProjects() {

        this.projects = [];

        if (!this.getInstance().isLoading()) {
            this.getInstance().fetch();
        }

    }

    updateProjectElement(project) {
        console.log("STORAGE UPD ACTIVITY:" + project.id)
        // Check if we already have this project in the state
        let index = this.projects.findIndex(function(projectElement) {
            if (projectElement.id === project.id) {
                return true;
            }
            return false;
        });
        /*  If we do we update it, otherwise we add a new
            project event to the state (at the top of the array) */
        if (index !== -1) {
            this.projects[index] = project;
        } else {
            this.projects.unshift(project);
        }

        this.errorMessage = null;
        // optionally return false to suppress the store change event
    }

    updateProjects(projects) {
        if (projects.hasOwnProperty('data')) {
            this.projects = projects.data.result;
        } else {
            this.projects = projects;
        }
    }

    selectProject(project) {
        if (this.selected != project) {
            this.selected = project;
        } else {
            this.selected = null;
        }
    }

}


module.exports = alt.createStore(ProjectsStore, 'ProjectsStore');

