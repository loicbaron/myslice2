import alt from '../alt';
import actions from '../actions/ProjectsActions';
import source from '../sources/ProjectsSource';

var removeFromArray = function(myArray, searchTerm, property=null) {
        for(var i = 0, len = myArray.length; i < len; i++) {
            if(property==null){
                var a = myArray[i];
            }else{
                var a = myArray[i][property];
            }
            if (a === searchTerm){
                myArray.splice(i, 1);
                return myArray;
            }
        }
        return myArray;
};

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

        this.addUserToProject = null;
        this.removeUserFromProject = null;
        this.removedUsers = {};

        this.deleteSliceFromProject = null;
        this.deletedSlices = {};

        this.dialog = null;

        this.errorMessage = null;

        this.bindListeners({
            updateProjectElement: actions.UPDATE_PROJECT_ELEMENT,
            updateProjects: actions.UPDATE_PROJECTS,
            setCurrentProject: actions.SET_CURRENT_PROJECT,
            updateUsers: actions.UPDATE_USERS,
            addUser: actions.ADD_USER,
            updateAddUser: actions.UPDATE_ADD_USER,
            errorAddUser: actions.ERROR_ADD_USER,

            removeUser: actions.REMOVE_USER,
            updateRemoveUser: actions.UPDATE_REMOVE_USER,
            errorRemoveUser: actions.ERROR_REMOVE_USER,

            deleteSlice: actions.DELETE_SLICE,
            updateDeleteSlice: actions.UPDATE_DELETE_SLICE,
            errorDeleteSlice: actions.ERROR_DELETE_SLICE,

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
        if(!(project.id in this.removedUsers)){
            this.removedUsers[project.id] = [];
        }
        if(!(project.id in this.deletedSlices)){
            this.deletedSlices[project.id] = [];
        }

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
    addUser(user) {
        this.addUserToProject = user;
        this.getInstance().addUser();
    }
    updateAddUser(message) {
        this.current.users.push(this.addUserToProject);
        this.addUserToProject=null;
    }
    errorAddUser(errorMessage) {
        console.log(errorMessage);
    }

    removeUser(user) {
        console.log(user);
        this.removeUserFromProject = user;
        this.getInstance().removeUser();
    }
    updateRemoveUser(message) {
        console.log(message);
        this.removedUsers[this.current.project.id].push(this.removeUserFromProject);
        this.current.project.pi_users = removeFromArray(this.current.project.pi_users, this.removeUserFromProject.id);
        this.removeUserFromProject=null;
        //this.current.users = removeFromArray(this.current.users, this.removeUserFromProject.id, 'id');
    }
    errorRemoveUser(errorMessage) {
        console.log(errorMessage);
    }

    deleteSlice(slice) {
        this.deleteSliceFromProject = slice;
        this.getInstance().deleteSlice();
    }
    updateDeleteSlice(message) {
        this.deletedSlices[this.current.project.id].push(this.deleteSliceFromProject);
        this.current.project.pi_users = removeFromArray(this.current.project.pi_users, this.deleteSliceFromProject.id);
        this.deleteSliceFromProject=null;
    }
    errorDeleteSlice(errorMessage) {
        console.log(errorMessage);
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

