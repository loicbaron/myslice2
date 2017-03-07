import alt from '../../alt';

class ProjectsActions {

    constructor() {
        this.generateActions(
            'addUsers',

            'fetchProjects',
            'updateProjectElement',
            'setCurrentProject',
            'updateProjects',
            'errorProjects',
            'updateUsers',
            'addUser',
            'updateAddUser',
            'errorAddUser',
            'removeUser',
            'updateRemoveUser',
            'errorRemoveUser',
            'deleteSlice',
            'updateDeleteSlice',
            'errorDeleteSlice',
            'errorUsers',
            'updateSlices',
            'errorSlices',

            'showDialog',
            'closeDialog',

            'deleteProject',
            'updateDeleteProject',
            'errorDeleteProject',


            'saveProject',
            'saveProjectSuccess',
            'saveProjectError'
        );
    }

}

export default alt.createActions(ProjectsActions);


