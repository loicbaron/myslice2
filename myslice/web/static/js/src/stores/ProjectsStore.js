import alt from '../alt';
import actions from '../actions/ProjectsActions';
import source from '../sources/ProjectsSource';

class ProjectsStore {

    constructor() {

        this.projects = [];

        /* the currently active project */
        this.current = {
            project: null,
            users: [],
            slices: []
        };

        this.filter = [];

        this.dialog = null;

        this.errorMessage = null;

        this.bindListeners({
            updateProjectElement: actions.UPDATE_PROJECT_ELEMENT,
            updateProjects: actions.UPDATE_PROJECTS,
            setCurrentProject: actions.SET_CURRENT_PROJECT,
            updateUsers: actions.UPDATE_USERS,
            updateSlices: actions.UPDATE_SLICES,
            fetchProjects: actions.FETCH_PROJECTS,
            errorProjects: actions.ERROR_PROJECTS,
            showDialog: actions.SHOW_DIALOG,
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
        let index = this.projects.findIndex(function(projectElement) {
            return (projectElement.id === project.id);
        });

        if (index !== -1) {
            this.projects[index] = project;
        } else {
            this.projects.unshift(project);
        }

        this.errorMessage = null;
    }

    setCurrentProject(project) {
        this.current.users = [];
        this.current.slices = [];
        this.current.project = project;

        if (!this.getInstance().isLoading()) {
            this.getInstance().users();
            this.getInstance().slices();
        }
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

    updateUsers(users) {
        if (users.hasOwnProperty('data')) {
            this.current.users = users.data.result;
        } else {
            this.current.users = users;
        }
    }

    errorUsers(errorMessage) {
        console.log(errorMessage);
    }

    updateSlices(slices) {
        if (slices.hasOwnProperty('data')) {
            this.current.slices = slices.data.result;
        } else {
            this.current.slices = slices;
        }
    }

    errorSlices(errorMessage) {
        console.log(errorMessage);
    }

    showDialog(dialog) {
        this.dialog = dialog;
    }
}


export default alt.createStore(ProjectsStore, 'ProjectsStore');

