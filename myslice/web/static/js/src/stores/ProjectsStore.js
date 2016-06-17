import alt from '../alt';
import actions from '../actions/ProjectsActions';
import source from '../sources/ProjectsSource';

class ProjectsStore {

    constructor() {
        this.projects = [];
        this.filter = {};
        this.errorMessage = null;

        this.bindListeners({
            updateProjectElement: actions.UPDATE_PROJECT_ELEMENT,

            updateProjects: actions.UPDATE_PROJECTS,
            fetchProjects: actions.FETCH_PROJECTS,
            errorProjects: actions.ERROR_PROJECTS
            
        });

        this.registerAsync(source);
    }

    fetchProjects(filter) {

        this.filter = filter;

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

    errorProjects(errorMessage) {
        console.log(errorMessage);
    } 

}


export default alt.createStore(ProjectsStore, 'ProjectsStore');

