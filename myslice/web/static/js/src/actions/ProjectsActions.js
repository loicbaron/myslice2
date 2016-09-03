import alt from '../alt';

class ProjectsActions {

    fetchProjects(filter = {}) {
        return filter;
    }

    updateProjectElement(project) {
        return project;
    }

    setCurrentProject(project) {
        return project;
    }

    updateProjects(project) {
        return project;
    }

    errorProjects(errorMessage) {
        return errorMessage
    }

    updateUsers(users) {
        return users;
    }

    addUser(user) {
        return user;
    }
    updateAddUser(message) {
        return message;
    }
    errorAddUser(errorMessage) {
        return errorMessage
    }

    removeUser(user) {
        return user;
    }
    updateRemoveUser(message) {
        return message;
    }
    errorRemoveUser(errorMessage) {
        return errorMessage
    }

    deleteSlice(slice) {
        return slice;
    }
    updateDeleteSlice(message) {
        return message;
    }
    errorDeleteSlice(errorMessage) {
        return errorMessage
    }

    errorUsers(errorMessage) {
        return errorMessage
    }

    updateSlices(slices) {
        return slices;
    }

    errorSlices(errorMessage) {
        return errorMessage
    }

    showDialog(dialog) {
        return dialog;
    }

    deleteProject(project) {
        return project
    }
    updateDeleteProject(project) {
        return project
    }
    errorDeleteProject(project) {
        return project
    }
}

export default alt.createActions(ProjectsActions);


