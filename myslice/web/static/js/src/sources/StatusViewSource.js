import axios from 'axios';
import actions from '../actions/views/Status';

const StatusViewSource = () => {
    return {
        testbeds: {
            remote(state) {
                return axios.get('/api/v1/testbeds');
            },

            // this function checks in our local cache first
            // if the value is present it'll use that instead (optional).
            // local(state) {
            //     return state.authorities ? state.authorities : null;
            // },

            // here we setup some actions to handle our response
            //loading: actions.loadingResults, // (optional)
            success: actions.updateTestbeds, // (required)
            error: actions.errorTestbeds, // (required)

            // should fetch has precedence over the value returned by local in determining whether remote should be called
            // in this particular example if the value is present locally it would return but still fire off the remote request (optional)
            shouldFetch(state) {
                return true
            }
        },

        resources: {
            remote(state) {
                return axios.get('/api/v1/testbeds/'+state.currentTestbed.id+'/resources');
            },

            success: actions.updateResources,
            error: actions.errorResources,

            shouldFetch(state) {
                return true
            }
        }
    }
};

export default StatusViewSource;

