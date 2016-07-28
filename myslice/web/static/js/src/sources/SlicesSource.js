import axios from 'axios';
import actions from '../actions/SliceViewActions';
import formactions from '../actions/SlicesFormActions';

const SlicesSource = () => {
    return {
        fetch: {
            remote(state) {
                /*
                    fetch the slices of the user
                 */
                return axios.get('/api/v1/users/slices');

            },

            // this function checks in our local cache first
            // if the value is present it'll use that instead (optional).
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
        submit: {
            // remotely fetch something (required)
            remote(state) {
                return axios.post('/api/v1/slices', {
                        'label': state.label,
                        'shortname':  state.name,
                        'project': state.project,
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

export default SlicesSource;

