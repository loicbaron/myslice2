'use strict';

Object.defineProperty(exports, "__esModule", {
    value: true
});

var _axios = require('axios');

var _axios2 = _interopRequireDefault(_axios);

var _DashboardActions = require('../actions/DashboardActions');

var _DashboardActions2 = _interopRequireDefault(_DashboardActions);

var _ProjectsFormActions = require('../actions/ProjectsFormActions');

var _ProjectsFormActions2 = _interopRequireDefault(_ProjectsFormActions);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

var DashboardSource = function DashboardSource() {
    return {
        fetch: {
            remote: function remote(state) {

                return _axios2.default.get('/api/v1/projects');
            },


            // this function checks in our local cache first
            // if the value is present it'll use that instead (optional).
            // local(state) {
            //     return state.authorities ? state.authorities : null;
            // },

            // here we setup some actions to handle our response
            //loading: actions.loadingResults, // (optional)
            success: _DashboardActions2.default.updateProjects, // (required)
            error: _DashboardActions2.default.errorProjects, // (required)

            // should fetch has precedence over the value returned by local in determining whether remote should be called
            // in this particular example if the value is present locally it would return but still fire off the remote request (optional)
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


            // should fetch has precedence over the value returned by local in determining whether remote should be called
            // in this particular example if the value is present locally it would return but still fire off the remote request (optional)
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
}; /**
    * Created by amirabradai on 17/10/2016.
    */
exports.default = DashboardSource;

//# sourceMappingURL=DashboardSource-compiled.js.map