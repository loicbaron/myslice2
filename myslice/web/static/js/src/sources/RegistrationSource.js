var axios = require('axios');
var actions = require('../actions/RegistrationActions');

module.exports = function() {
    return {
        submit: {
            // remotely fetch something (required)
            remote(state) {
                return axios.post('/api/v1/users', {
                    'authority': state.authority,
                    'firstname': state.firstname,
                    'lastname': state.lastname,
                    'email': state.email
                });
            },

            // this function checks in our local cache first
            // if the value is present it'll use that instead (optional).
            // local(state) {
            //     return state.authorities ? state.authorities : null;
            // },

            // here we setup some actions to handle our response
            //loading: actions.loading, // (optional)
            success: actions.submitSuccess, // (required)
            error: actions.submitError, // (required)

            // should fetch has precedence over the value returned by local in determining whether remote should be called
            // in this particular example if the value is present locally it would return but still fire off the remote request (optional)
            shouldFetch(state) {
                return true
            }
        }
    }
};