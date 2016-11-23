import axios from 'axios';
import actions from '../actions/ProjectsActions';
import formactions from '../actions/ProjectsFormActions';

const ProjectsSource = () => {
    return {
        fetch: {

            remote(state) {
                var type = null;
                switch(type) {
                    case 'authority':
                        return axios.get('/api/v1/authorities/projects');
                    default:
                        return axios.get('/api/v1/projects');
                }

            },

            // this function checks in our local cache first
            // if the value is present it'll use that instead (optional).
            // local(state) {
            //     return state.authorities ? state.authorities : null;
            // },

            // here we setup some actions to handle our response
            //loading: actions.loadingResults, // (optional)
            success: actions.updateProjects, // (required)
            error: actions.errorProjects, // (required)

            // should fetch has precedence over the value returned by local in determining whether remote should be called
            // in this particular example if the value is present locally it would return but still fire off the remote request (optional)
            shouldFetch(state) {
                return true
            }
        },

        users: {

            remote(state) {
                if (state.current.project) {
                    return axios.get('/api/v1/projects/' + state.current.project.id + '/users');
                }

            },

            // local(state) {
            //     return state.authorities ? state.authorities : null;
            // },

            // here we setup some actions to handle our response
            //loading: actions.loadingResults, // (optional)
            success: actions.updateUsers, // (required)
            error: actions.errorUsers, // (required)

            // should fetch has precedence over the value returned by local in determining whether remote should be called
            // in this particular example if the value is present locally it would return but still fire off the remote request (optional)
            shouldFetch(state) {
                return true
            }
        },

        saveProject: {

            remote(state) {
                if (state.saving) {
                    return axios.put('/api/v1/projects/' + state.current.project.id, state.saving);
                }

            },

            // local(state) {
            //     return state.authorities ? state.authorities : null;
            // },

            // here we setup some actions to handle our response
            //loading: actions.loadingResults, // (optional)
            success: actions.successSave, // (required)
            error: actions.errorSave, // (required)

            // should fetch has precedence over the value returned by local in determining whether remote should be called
            // in this particular example if the value is present locally it would return but still fire off the remote request (optional)
            shouldFetch(state) {
                return true
            }
        },

        addUser: {

            remote(state) {
                return axios.put('/api/v1/projects/' + state.current.project.id, {'action':'add','users':[state.addUserToProject.id]});
            },

            success: actions.updateAddUser, // (required)
            error: actions.errorAddUser, // (required)

            shouldFetch(state) {
                return true
            }
        },
        removeUser: {

            remote(state) {
                return axios.put('/api/v1/projects/' + state.current.project.id, {'action':'remove','users':[state.removeUserFromProject.id]});
            },

            success: actions.updateRemoveUser, // (required)
            error: actions.errorRemoveUser, // (required)

            shouldFetch(state) {
                return true
            }
        },

        deleteSlice: {

            remote(state) {
                return axios.delete('/api/v1/slices/' + state.deleteSliceFromProject.id);
            },

            success: actions.updateDeleteSlice, // (required)
            error: actions.errorDeleteSlice, // (required)

            shouldFetch(state) {
                return true
            }
        },

        slices: {

            remote(state) {
                if (state.current.project) {
                    return axios.get('/api/v1/projects/' + state.current.project.id + '/slices');
                }

            },

            // local(state) {
            //     return state.authorities ? state.authorities : null;
            // },

            // here we setup some actions to handle our response
            //loading: actions.loadingResults, // (optional)
            success: actions.updateSlices, // (required)
            error: actions.errorSlices, // (required)

            // should fetch has precedence over the value returned by local in determining whether remote should be called
            // in this particular example if the value is present locally it would return but still fire off the remote request (optional)
            shouldFetch(state) {
                return true
            }
        },

        deleteProject: {

            remote(state) {
                return axios.delete('/api/v1/projects/' + state.deleteProj.id);
            },

            success: actions.updateDeleteProject, // (required)
            error: actions.errorDeleteProject, // (required)

            shouldFetch(state) {
                return true
            }
        },

        submit: {
            // remotely fetch something (required)
            remote(state) {
                var v = 'public';
                if (state.v_public) v = 'public';
                if (state.v_protected) v = 'protected';
                if (state.v_private) v = 'private';
                return axios.post('/api/v1/projects', {
                        'label': state.label,
                        'name':  state.name,
                        'authority': state.authority,
                        'visibility': v,
                        'url': state.url,
                        'description': state.description,
                        'start_date': state.start_date,
                        'end_date': state.end_date,
                    });
            },

            // this function checks in our local cache first
            // if the value is present it'll use that instead (optional).
            // local(state) {
            //     return state.authorities ? state.authorities : null;
            // },

            // here we setup some actions to handle our response
            //loading: actions.loading, // (optional)
            success: formactions.submitSuccess, // (required)
            error: formactions.submitError, // (required)

            // should fetch has precedence over the value returned by local in determining whether remote should be called
            // in this particular example if the value is present locally it would return but still fire off the remote request (optional)
            shouldFetch(state) {
                return true
            }
        }
    }
};

export default ProjectsSource;

