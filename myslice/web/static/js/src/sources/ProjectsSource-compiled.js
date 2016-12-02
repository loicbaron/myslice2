'use strict';

Object.defineProperty(exports, "__esModule", {
    value: true
});

var _axios = require('axios');

var _axios2 = _interopRequireDefault(_axios);

var _ProjectsActions = require('../actions/ProjectsActions');

var _ProjectsActions2 = _interopRequireDefault(_ProjectsActions);

var _ProjectsFormActions = require('../actions/ProjectsFormActions');

var _ProjectsFormActions2 = _interopRequireDefault(_ProjectsFormActions);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

var ProjectsSource = function ProjectsSource() {
    return {
        fetch: {
            remote: function remote(state) {
                var type = null;
                switch (type) {
                    case 'authority':
                        return _axios2.default.get('/api/v1/authorities/projects');
                    default:
                        return _axios2.default.get('/api/v1/projects');
                }
            },


            // this function checks in our local cache first
            // if the value is present it'll use that instead (optional).
            // local(state) {
            //     return state.authorities ? state.authorities : null;
            // },

            // here we setup some actions to handle our response
            //loading: actions.loadingResults, // (optional)
            success: _ProjectsActions2.default.updateProjects, // (required)
            error: _ProjectsActions2.default.errorProjects, // (required)

            // should fetch has precedence over the value returned by local in determining whether remote should be called
            // in this particular example if the value is present locally it would return but still fire off the remote request (optional)
            shouldFetch: function shouldFetch(state) {
                return true;
            }
        },

        users: {
            remote: function remote(state) {
                if (state.current.project) {
                    return _axios2.default.get('/api/v1/projects/' + state.current.project.id + '/users');
                }
            },


            // local(state) {
            //     return state.authorities ? state.authorities : null;
            // },

            // here we setup some actions to handle our response
            //loading: actions.loadingResults, // (optional)
            success: _ProjectsActions2.default.updateUsers, // (required)
            error: _ProjectsActions2.default.errorUsers, // (required)

            // should fetch has precedence over the value returned by local in determining whether remote should be called
            // in this particular example if the value is present locally it would return but still fire off the remote request (optional)
            shouldFetch: function shouldFetch(state) {
                return true;
            }
        },
        addUser: {
            remote: function remote(state) {
                return _axios2.default.put('/api/v1/projects/' + state.current.project.id, { 'action': 'add', 'users': [state.addUserToProject.id] });
            },


            success: _ProjectsActions2.default.updateAddUser, // (required)
            error: _ProjectsActions2.default.errorAddUser, // (required)

            shouldFetch: function shouldFetch(state) {
                return true;
            }
        },
        removeUser: {
            remote: function remote(state) {
                return _axios2.default.put('/api/v1/projects/' + state.current.project.id, { 'action': 'remove', 'users': [state.removeUserFromProject.id] });
            },


            success: _ProjectsActions2.default.updateRemoveUser, // (required)
            error: _ProjectsActions2.default.errorRemoveUser, // (required)

            shouldFetch: function shouldFetch(state) {
                return true;
            }
        },

        deleteSlice: {
            remote: function remote(state) {
                return _axios2.default.delete('/api/v1/slices/' + state.deleteSliceFromProject.id);
            },


            success: _ProjectsActions2.default.updateDeleteSlice, // (required)
            error: _ProjectsActions2.default.errorDeleteSlice, // (required)

            shouldFetch: function shouldFetch(state) {
                return true;
            }
        },

        slices: {
            remote: function remote(state) {
                if (state.current.project) {
                    return _axios2.default.get('/api/v1/projects/' + state.current.project.id + '/slices');
                }
            },


            // local(state) {
            //     return state.authorities ? state.authorities : null;
            // },

            // here we setup some actions to handle our response
            //loading: actions.loadingResults, // (optional)
            success: _ProjectsActions2.default.updateSlices, // (required)
            error: _ProjectsActions2.default.errorSlices, // (required)

            // should fetch has precedence over the value returned by local in determining whether remote should be called
            // in this particular example if the value is present locally it would return but still fire off the remote request (optional)
            shouldFetch: function shouldFetch(state) {
                return true;
            }
        },

        deleteProject: {
            remote: function remote(state) {
                return _axios2.default.delete('/api/v1/projects/' + state.deleteProj.id);
            },


            success: _ProjectsActions2.default.updateDeleteProject, // (required)
            error: _ProjectsActions2.default.errorDeleteProject, // (required)

            shouldFetch: function shouldFetch(state) {
                return true;
            }
        },

        submit: {
            // remotely fetch something (required)
            remote: function remote(state) {
                var v = 'public';
                if (state.v_public) v = 'public';
                if (state.v_protected) v = 'protected';
                if (state.v_private) v = 'private';
                return _axios2.default.post('/api/v1/projects', {
                    'label': state.label,
                    'name': state.name,
                    'authority': state.authority,
                    'visibility': v,
                    'url': state.url,
                    'description': state.description,
                    'start_date': state.start_date,
                    'end_date': state.end_date
                });
            },


            // this function checks in our local cache first
            // if the value is present it'll use that instead (optional).
            // local(state) {
            //     return state.authorities ? state.authorities : null;
            // },

            // here we setup some actions to handle our response
            //loading: actions.loading, // (optional)
            success: _ProjectsFormActions2.default.submitSuccess, // (required)
            error: _ProjectsFormActions2.default.submitError, // (required)

            // should fetch has precedence over the value returned by local in determining whether remote should be called
            // in this particular example if the value is present locally it would return but still fire off the remote request (optional)
            shouldFetch: function shouldFetch(state) {
                return true;
            }
        }
    };
};

exports.default = ProjectsSource;

//# sourceMappingURL=ProjectsSource-compiled.js.map